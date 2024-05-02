// This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK (v2).
// Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
// session persistence, api calls, and more.
const Alexa = require('ask-sdk-core');
const persistenceAdapter = require('ask-sdk-s3-persistence-adapter');
const { sendEmailNotification } = require('./emailSender');
const { getNextTask, getDiffToStartDate } = require('./reminders.js');

const APP_NAME = "Template Seven";
const messages = {
  NOTIFY_MISSING_PERMISSIONS: 'Please enable profile permissions in the Amazon Alexa app.',
  ERROR: 'Uh Oh. Looks like something went wrong.'
};

const FULL_NAME_PERMISSION = "alexa::profile:name:read";
const EMAIL_PERMISSION = "alexa::profile:email:read";
const MOBILE_PERMISSION = "alexa::profile:mobile_number:read";

const LaunchRequestHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'LaunchRequest';
    },
    async handle(handlerInput) {
        const attributesManager = handlerInput.attributesManager;
        const sessionAttributes = attributesManager.getSessionAttributes() || {};
        const userName = sessionAttributes.hasOwnProperty('name') ? sessionAttributes.name : "";

        const speakOutput = userName
            ? `Welcome ${userName}, when is your start date?`
            : 'Hello! Welcome to Amazon Intern Helper. What is your name?';
            
        const repromptText = 'I\'m excited to hear that you\'ll be starting at Amazon. When is your start date?';
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(repromptText)
            .getResponse();
        
    }
};

const EmailIntentHandler = {
  canHandle(handlerInput) {
    return handlerInput.requestEnvelope.request.type === 'IntentRequest'
      && handlerInput.requestEnvelope.request.intent.name === 'EmailIntent';
  },
  async handle(handlerInput) {
    const { serviceClientFactory, responseBuilder } = handlerInput;
    try {
      const upsServiceClient = serviceClientFactory.getUpsServiceClient();
      const profileEmail = await upsServiceClient.getProfileEmail();
      if (!profileEmail) {
        const noEmailResponse = `It looks like you don't have an email set. You can set your email from the companion app.`
        return responseBuilder
                      .speak(noEmailResponse)
                      .withSimpleCard(APP_NAME, noEmailResponse)
                      .getResponse();
      }
      const speechResponse = `Your email is, ${profileEmail}`;
      return responseBuilder
                      .speak(speechResponse)
                      .withSimpleCard(APP_NAME, speechResponse)
                      .reprompt(speechResponse)
                      .getResponse();
    } catch (error) {
      console.log(JSON.stringify(error));
      if (error.statusCode === 403) {
        return responseBuilder
        .speak(messages.NOTIFY_MISSING_PERMISSIONS)
        .withAskForPermissionsConsentCard([EMAIL_PERMISSION])
        .getResponse();
      }
      console.log(JSON.stringify(error));
      const response = responseBuilder.speak(messages.ERROR).getResponse();
      return response;
    }
  },
}

const getEmail = async (handlerInput) => {
    const response = {error: true, message: null, email: null};
    const { serviceClientFactory, responseBuilder } = handlerInput;
    try {
      const upsServiceClient = serviceClientFactory.getUpsServiceClient();
      const profileEmail = await upsServiceClient.getProfileEmail();
      if (!profileEmail) {
        response.message = `It looks like you don't have an email set. You can set your email from the Alexa companion app.`;
        return response;
      } else response.error = false;
      response.email = profileEmail;
      return response;
    } catch (error) {
      if (error.statusCode === 403) response.message = messages.NOTIFY_MISSING_PERMISSIONS;
      return response;
    }
}


const HasNameDateLaunchRequestHandler = {
    canHandle(handlerInput) {
        console.log(JSON.stringify(handlerInput.requestEnvelope.request));
        const attributesManager = handlerInput.attributesManager;
        const sessionAttributes = attributesManager.getSessionAttributes() || {};
        
        const userName = sessionAttributes.hasOwnProperty('name') ? sessionAttributes.name : "";
        const startDate = sessionAttributes.hasOwnProperty('startDate') ? sessionAttributes.startDate : 0;
        
        return handlerInput.requestEnvelope.request.type === 'LaunchRequest' &&
            userName &&
            startDate;
    },
    async handle(handlerInput) {
        const attributesManager = handlerInput.attributesManager;
        const sessionAttributes = attributesManager.getSessionAttributes() || {};
        const userName = sessionAttributes.hasOwnProperty('name') ? sessionAttributes.name : "";
        const diffDays = await getDiffToStartDate(handlerInput);
        const speakOutput = `Welcome back ${userName}. It looks like there are ${diffDays} days until your start date.`

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(speakOutput)
            .getResponse();
    }
};


const CaptureUserNameHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'CaptureUserNameIntent';
    },
    async handle(handlerInput) {
        const userName = handlerInput.requestEnvelope.request.intent.slots.name.value;
        const attributesManager = handlerInput.attributesManager;
        const sessionAttributes = attributesManager.getSessionAttributes() || {};
        
        sessionAttributes.name = userName;
        attributesManager.setPersistentAttributes(sessionAttributes);
        await attributesManager.savePersistentAttributes(); 

        const date = sessionAttributes.hasOwnProperty('startDate') ? sessionAttributes.startDate : 0;
        let speakOutput; 
        if (date){
            speakOutput = `Thanks ${userName}, your start date is ${date.month} ${date.day}, ${date.year}.`
        } else {
            speakOutput = `Thanks ${userName}, when is your start date?`;
        }

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt('When is your start date?')
            .getResponse();
    }
};

const CaptureStartDateIntentHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'CaptureStartDateIntent';
    },
    async handle(handlerInput) {
        const year = handlerInput.requestEnvelope.request.intent.slots.year.value;
        const month = handlerInput.requestEnvelope.request.intent.slots.month.value;
        const day = handlerInput.requestEnvelope.request.intent.slots.day.value;
        
        const attributesManager = handlerInput.attributesManager;
        const sessionAttributes = attributesManager.getSessionAttributes() || {};
        const userName = sessionAttributes.hasOwnProperty('name') ? sessionAttributes.name : "";
        
        const startDateAttributes = {
            "year": year,
            "month": month,
            "day": day   
        };
        sessionAttributes.startDate = startDateAttributes;
        
        attributesManager.setPersistentAttributes(sessionAttributes);
        await attributesManager.savePersistentAttributes();    
        
        
        const speakOutput = `Thanks ${userName}, I'll remember that you will start on ${month} ${day} ${year}.`;
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(speakOutput)
            .getResponse();
    }
};

/*
 * Handles retrieving the "latest" task, in a sort of "stack" style, for the intern to complete.
 * If the intern completed the task and lets us know, we store it and not ask the intern about that task again.
*/
const WhatToDoNextIntentHandler = {
    canHandle(handlerInput) {
        const request = handlerInput.requestEnvelope.request;
        return request.type === 'IntentRequest'
            && request.intent.name === 'WhatToDoNextIntent';
            
    },
    async handle(handlerInput) {
        const [nextTask, speakOutput] = await getNextTask(handlerInput);

        if (nextTask !== 'NONE') {
            const attributesManager = handlerInput.attributesManager;
            const sessionAttributes = attributesManager.getSessionAttributes() || {};
            sessionAttributes.taskType = nextTask;
            sessionAttributes.sessionState = "check_task_completed";
            attributesManager.setPersistentAttributes(sessionAttributes);
            await attributesManager.savePersistentAttributes();
        }
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(speakOutput)
            .getResponse();
    }
};

const YesIntentHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'AMAZON.YesIntent';
    },

    async handle(handlerInput){
        const attributesManager = handlerInput.attributesManager;
        const sessionAttributes = attributesManager.getSessionAttributes();
        const task = sessionAttributes.taskType;
        const userName = sessionAttributes.name;
        let speakOutput;
        switch(sessionAttributes.sessionState) {
            case "check_task_completed":
                speakOutput = 'Awesome!';
                sessionAttributes.sessionState = "default";
                sessionAttributes[task] = true;
                attributesManager.setPersistentAttributes(sessionAttributes);
                await attributesManager.savePersistentAttributes();
                break;
            
            case "send_email":
                const email = await getEmail(handlerInput);
                if (email.error) {
                    return EmailIntentHandler.handle(handlerInput);
                }
                const userInfo = {
                    userName: userName,
                    emailAddress: email.email
                }
                const emailResponse = sendEmailNotification(task, userInfo);
                if (emailResponse.error) {
                    // error, don't save that the task is completed, just let the user know that there was an email-related error
                    speakOutput = `Sorry, ${userName}, there was a problem with sending the email. Please try again later!`;
                } else {
                    speakOutput = `Alright, ${userName}, I've sent them an email! Hopefully you hear about it soon.`;
                    sessionAttributes[task] = true;
                    sessionAttributes.sessionState = "default";
                    attributesManager.setPersistentAttributes(sessionAttributes);
                    await attributesManager.savePersistentAttributes();
                }
                break
            
            default:
                speakOutput = 'Sorry, this is an invalid answer. Please try again.'

        }
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(speakOutput)
            .getResponse();

    }

}

const NoIntentHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'AMAZON.NoIntent';
    },
    async handle(handlerInput){
        const attributesManager = handlerInput.attributesManager;
        const sessionAttributes = attributesManager.getSessionAttributes();
        const task = sessionAttributes.taskType;
        let speakOutput;
        switch(sessionAttributes.sessionState) {
            case "check_task_completed":
                speakOutput = 'Ok. I can send an email to Amazon for you to help you with this. Would you like that?';
                sessionAttributes.sessionState = "send_email";
                attributesManager.setPersistentAttributes(sessionAttributes);
                await attributesManager.savePersistentAttributes();
                break;
            case "send_email":
                speakOutput = 'OK, I will not contact them';
                sessionAttributes.sessionState = "default";
                attributesManager.setPersistentAttributes(sessionAttributes);
                await attributesManager.savePersistentAttributes();
                break;
            default:
                speakOutput = 'Sorry, this is an invalid answer. Please try again.'
        }
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(speakOutput)
            .getResponse();
    }

}


const HelpIntentHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'AMAZON.HelpIntent';
    },
    handle(handlerInput) {
        const speakOutput = 'You can say hello to me! How can I help?';

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(speakOutput)
            .getResponse();
    }
};
const CancelAndStopIntentHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && (handlerInput.requestEnvelope.request.intent.name === 'AMAZON.CancelIntent'
                || handlerInput.requestEnvelope.request.intent.name === 'AMAZON.StopIntent');
    },
    handle(handlerInput) {
        const speakOutput = 'Goodbye!';
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .getResponse();
    }
};
const SessionEndedRequestHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'SessionEndedRequest';
    },
    handle(handlerInput) {
        // Any cleanup logic goes here.
        return handlerInput.responseBuilder.getResponse();
    }
};

// The intent reflector is used for interaction model testing and debugging.
// It will simply repeat the intent the user said. You can create custom handlers
// for your intents by defining them above, then also adding them to the request
// handler chain below.
const IntentReflectorHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest';
    },
    handle(handlerInput) {
        const intentName = handlerInput.requestEnvelope.request.intent.name;
        const speakOutput = `You just triggered ${intentName}`;

        return handlerInput.responseBuilder
            .speak(speakOutput)
            //.reprompt('add a reprompt if you want to keep the session open for the user to respond')
            .getResponse();
    }
};

// Generic error handling to capture any syntax or routing errors. If you receive an error
// stating the request handler chain is not found, you have not implemented a handler for
// the intent being invoked or included it in the skill builder below.
const ErrorHandler = {
    canHandle() {
        return true;
    },
    handle(handlerInput, error) {
        console.log(`~~~~ Error handled: ${error.message}`);
        const speakOutput = `Sorry, I couldn't understand what you said. Please try again.`;

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(speakOutput)
            .getResponse();
    }
};


const LoadStorageInterceptor = {
    async process(handlerInput) {
        const attributesManager = handlerInput.attributesManager;
        const sessionAttributes = await attributesManager.getPersistentAttributes() || {};
        const name = sessionAttributes.hasOwnProperty('name') ? sessionAttributes.name : "";
        const date = sessionAttributes.hasOwnProperty('startDate') ? sessionAttributes.startDate : {};

        if (name || date) {
            attributesManager.setSessionAttributes(sessionAttributes);
        }
    }
}

// The SkillBuilder acts as the entry point for your skill, routing all request and response
// payloads to the handlers above. Make sure any new handlers or interceptors you've
// defined are included below. The order matters - they're processed top to bottom.
exports.handler = Alexa.SkillBuilders.custom()
    .withPersistenceAdapter(
        new persistenceAdapter.S3PersistenceAdapter({bucketName:process.env.S3_PERSISTENCE_BUCKET})
    )
    .addRequestHandlers(
        HasNameDateLaunchRequestHandler,
        LaunchRequestHandler,
        WhatToDoNextIntentHandler,
        YesIntentHandler,
        NoIntentHandler,
        CaptureUserNameHandler,
        EmailIntentHandler,
        CaptureStartDateIntentHandler,
        HelpIntentHandler,
        CancelAndStopIntentHandler,
        SessionEndedRequestHandler,
        IntentReflectorHandler) // make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
    .addErrorHandlers(
        ErrorHandler)
    .addRequestInterceptors(
        LoadStorageInterceptor
    )
    .withApiClient(new Alexa.DefaultApiClient())
    .lambda();