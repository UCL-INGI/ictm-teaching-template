# ICTM Teaching

## Configuring SAML authentication
### Setting up a fake SAML IdP server 

1. Create a working directory `<some_path>/saml-idp` and install the npm package `saml-idp`.

    ```shell
    [user@localhost saml-idp]$ npm install saml-idp
    ```
1. Create a pair of self-signed X.509 private key and certificate

    ```shell
    [user@localhost saml-idp]$ openssl req -newkey rsa:2048 -nodes -keyout idp_key.pem -x509 -days 365 -out idp_cert.pem
    ```
1. Create a `idp_config.js` file to contain the fake IdP configuration.
    ```javascript
        /**
        * User Profile
        */
        var profile = {
          userName: 'sjackson',
          nameIdFormat: 'urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified',
          uid: 'sjackson',
          lastName:'Jackson',
          firstName: 'Saml',
          email: 'saml.jackson@example.com'
        }

        /**
         * SAML Attribute Metadata
         */
        var metadata = [
        {
          id: "uid",
          optional: false,
          displayName: 'Username',
          description: 'The username of the user',
          multiValue: false
        },
        {
          id: "email",
          optional: false,
          displayName: 'E-Mail Address',
          description: 'The e-mail address of the user',
          multiValue: false
        },
        {
          id: "firstName",
          optional: false,
          displayName: 'First Name',
          description: 'The given name of the user',
          multiValue: false
        },
        {
          id: "lastName",
          optional: false,
          displayName: 'Last Name',
          description: 'The surname of the user',
          multiValue: false
        }];

        module.exports = {
          user: profile,
          metadata: metadata
        }
      ```
   Your working folder should contain `idp_key.pem`, `idp_cert.pem` and `idp_config.js`.
1. Run the IdP server by running (`acsUrl` points to the Teaching app and may change if you changed the port):
    ```shell
    node node_modules/saml-idp/bin/run.js --key ./key.pem --cert ./certificate.pem \
    --configFile <some_path>/saml-idp/idp_config.js --acsUrl http:/localhost:5000/auth/callback \
    --audience ictm-teaching --issuer saml-idp
    ```
    The `configFile` parameter requires an absolute path to work correctly. The server will run, by default, on port `7000`.

### Configuring the app (or SAML SP)

1. Create a pair of self-signed X.509 private key and certificate

    ```shell
    [user@localhost ictm-teaching]$ openssl req -newkey rsa:2048 -nodes -keyout sp_key.pem -x509 -days 365 -out sp_cert.pem
    ```

1. Adapt the `config.json`file so that the `SAML` corresponds to :
    ```javascript
      "SAML": {
          "attributes": {
            "sn": "lastName",
            "email": "email",
            "givenName": "firstName",
            "uid": "uid"
          },
          "security": {
            "metadataValidUntil": "",
            "metadataCacheDuration": "",
            "wantAssertionsEncrypted": false,
            "wantAssertionsSigned": true,
            "authnRequestsSigned": true
          },
          "sp": {
            "assertionConsumerService": {
              "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
            },
            "entityId": "ictm-teaching",
            "x509cert": "<paste sp_cert.pem here>",
            "privateKey": "<paste sp_key.pem here>"
          },
          "idp": {
            "entityId": "saml-idp",
            "singleSignOnService": {
              "url": "http://localhost:7000/saml/sso",
              "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
            },
            "x509cert": "<paste idp_cert.pem here>"
          },
          "strict": true
        }
     ```
     and paste the content of the required files in the indicated `<tags>`.
     
1. You can now run the app and feed any user information using the fields provided by the IdP application.
