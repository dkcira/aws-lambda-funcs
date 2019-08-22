exports.handler = function(event, context, callback){
    callback(null, "some success message");
    return {
        "statusCode": 200,
        "message": "This is the first NodeJS Lambda!"
    }
};