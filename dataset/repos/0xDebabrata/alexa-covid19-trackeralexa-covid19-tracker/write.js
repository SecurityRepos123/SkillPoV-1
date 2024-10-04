const AWS = require("aws-sdk")
const { accessKeyId, secretAccessKey } = auths.aws

// Passed to the step
const { region, TableName, item } = params;
const dynamodb = new AWS.DynamoDB({
  accessKeyId,
  secretAccessKey,
  region,
})

// Object template
let Item = {
  'country': {
    S:''
  },
  'totalCases': {
    S:''
  },
  'deaths': {
    S:''
  }
}

for (let j=0; j<item.length; j++){
  Object.keys(item[j]).forEach((key) => {
    if (key === 'country'){
      Item['country']['S'] = item[j][key]
    } else if (key === 'totalCases'){
      Item['totalCases']['S'] = item[j][key]
    } else {
      Item['deaths']['S'] = item[j][key]
    }
  })
  const payload = {
    Item,
    TableName
  }
  this.resp = await dynamodb.putItem(payload).promise()

}
