const EMAIL_TYPES = [
    ['BACKGROUND_CHECK_REQUEST', 45, 'By now, your background check should have been started. Did you receive a notice about it starting?'],
    ['IMMIGRATION_REQUEST', 30, 'You should have had a CPT letter uploaded to your candidate portal, if that applies to you. \
        If you already dealt with this or if this doesn\'t apply to you, please say Yes.'],
    ['MANAGER_CONTACT_REQUEST', 30, 'You should have been introduced to your manager and or team. Have you?'],
    ['RELOCATION_REQUEST', 30, 'You should have received a note from Graebel in-regards to relocation. Have you?'],
    ['MYDOCS_REQUEST', 14, 'By now, you should have received a MyDocs email. Have you already received it?'],
    ['NHO_REQUEST', 3, 'Since it \'s so close to your start date, you should have received an email from New Hire Support in regards to orientation. \
        Have you received this email?']
];
const setupTasks = async (handlerInput) => {
    const attributesManager = handlerInput.attributesManager;
    const sessionAttributes = await attributesManager.getPersistentAttributes() || {};

    const unsavedAttrs = EMAIL_TYPES.filter(([type, days]) => !sessionAttributes.hasOwnProperty(type));
    if (unsavedAttrs.length) {
        const intializeCompleted = {};
        EMAIL_TYPES.forEach(([type, days]) => intializeCompleted[type] = false);
        attributesManager.setPersistentAttributes(intializeCompleted);
        await attributesManager.savePersistentAttributes();
    }
};
const getNextTask = async (handlerInput, getKey=false) => {
    setupTasks(handlerInput);
    const days = await getDiffToStartDate(handlerInput);
    // const persistentAttrs = await handlerInput.attributesManager.getPersistentAttributes();
    const sessionAttributes = handlerInput.attributesManager.getSessionAttributes() || {};
    const notificationBin = EMAIL_TYPES.filter(([type, lateDayLimit, message]) => (days < lateDayLimit && !sessionAttributes[ type ]));
    const selectedTask = notificationBin[0];
    if (selectedTask) {
        // Set session attrs appropriately
        const [type, lateDayLimit, message] = selectedTask;
        const sessionAttributes = handlerInput.attributesManager.getSessionAttributes();
        sessionAttributes.taskType = type;
        handlerInput.attributesManager.setSessionAttributes(sessionAttributes);

        if (!getKey) return [type, message];
        return type;
    }
    return ['NONE', 'You have nothing to worry about!'];
};

async function getDiffToStartDate(handlerInput) {
    const serviceClientFactory = handlerInput.serviceClientFactory;
    const deviceId = handlerInput.requestEnvelope.context.System.device.deviceId;
    const attributesManager = handlerInput.attributesManager;
    const sessionAttributes = attributesManager.getSessionAttributes() || {};
    const date = sessionAttributes.hasOwnProperty('startDate') ? sessionAttributes.startDate : {};

    const startDate = Date.parse(`${date.month} ${date.day}, ${date.year}`);
    
    let userTimeZone;
    try {
        const upsServiceClient = serviceClientFactory.getUpsServiceClient();
        userTimeZone = await upsServiceClient.getSystemTimeZone(deviceId);
    } catch (error) {
        if (error.name !== 'ServiceError') {
            return handlerInput.responseBuilder.speak("There was a problem connecting to the service.").getResponse();
        }
        console.log('error', error.message);
    }
    console.log('userTimeZone', userTimeZone);

    const oneDay = 24 * 60 * 60 * 1000;

    // getting the current date with the time
    const currentDateTime = new Date(new Date().toLocaleString("en-US", { timeZone: userTimeZone }));
    // removing the time from the date because it affects our difference calculation
    const currentDate = new Date(currentDateTime.getFullYear(), currentDateTime.getMonth(), currentDateTime.getDate());
    const diffDays = Math.round((startDate - currentDate.getTime()) / oneDay);
    return diffDays

}

module.exports = Object.freeze({
  getNextTask, getDiffToStartDate
});
