const AWS = require('aws-sdk');

// Configure the AWS SDK (e.g., setting the region)
AWS.config.update({region: 'us-east-2'});

const sagemakerRuntime = new AWS.SageMakerRuntime();

const params = {
    EndpointName: 'remote-endpoint',
    Body: 'Translate to German: Hello, how are you?',
    ContentType: 'application/json'
};

sagemakerRuntime.invokeEndpoint(params, (err, data) => {
    if (err) {
        console.error("Error:", err);
    } else {
        const response = data.Body.toString('utf-8');
        console.log(response);
    }
});
