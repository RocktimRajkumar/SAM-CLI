# A simple token-based authorizer example to demonstrate how to use an authorization token 
# to allow or deny a request. In this example, the caller named 'user' is allowed to invoke 
# a request if the client-supplied token value is 'allow'. The caller is not allowed to invoke 
# the request if the token value is 'deny'. If the token value is 'unauthorized' or an empty
# string, the authorizer function returns an HTTP 401 status code. For any other token value, 
# the authorizer returns an HTTP 500 status code. 
# Note that token values are case-sensitive.

def authorizer(event, context):

    print(event)
    token = event['authorizationToken']
    if token == 'allow':
        return generatePolicy('user', 'Allow', event['methodArn'])
    elif token=='deny':
        return generatePolicy('user', 'Deny', event['methodArn'])
    else:
        raise Exception('Unauthorized')  # Return a 401 Unauthorized response

# Help function to generate an IAM policy
def generatePolicy(principalId, effect, resource):
    authResponse = {}
    
    authResponse['principalId'] = principalId
    if effect and resource:
        policyDocument = {}
        policyDocument['Version'] = '2012-10-17'
        policyDocument['Statement'] = []
        statementOne = {}
        statementOne['Action'] = 'execute-api:Invoke'
        statementOne['Effect'] = effect
        statementOne['Resource'] = resource
        policyDocument['Statement'].append(statementOne)
        authResponse['policyDocument'] = policyDocument
    
    return authResponse