const { subtle } = require("crypto").webcrypto; // Native Node Library
const Stomp = require("stompjs"); // Stomp Protocol Library



const xKey = "YOUR_X-KEY" // This is your KEY-ID relative to the PRIVATE KEY that you are using
const privateKeyBase64 = "YOUR_PRIVATE_KEY" // This is your PRIVATE_KEY shown as a base64 string when created in the application

// Import Your Base64 Private Key

const apiCallExample = async () => {
    // Your key is presented in Base64 format - It should be changed to the correct format
    const privateKey = await importPrivateKey(privateKeyBase64);

    const postBodyData =  (_bodyData) => _bodyData ? JSON.stringify(_bodyData) : ``;
    const queryParameter = (queryParams) => queryParams ? queryParams : ``;

    // Base Structure Of Payload Shape
    const signaturePayload = `Signature{body='', queryParam=''}`

    // If sending data in a Post it should be added as a stringified object
    // EXAMPLE: const signaturePayload = `Signature{body='JSON.stringify({hello: "world"})', queryParam=''}`
 
    // Query Parameters Are Added As Below
    // EXAMPLE: const signaturePayload = `Signature{body='', queryParam='hello=world'}`

    // Sign the Data
    const signature = await signPayload(privateKey, signaturePayload)

    // Change signature to Base 64
    const base64Signature = Buffer.from(signature).toString("base64")


    // Do an API Call As normal - Adding the following headers
    await axios.get("https://api.finxflo.com/me", {
      headers: {
        "x-key": devXkey,
        "x-signature": base64Signature,
      },
    })
}


// Websocket Example

const client = Stomp.overWS("wss://ws.finxflo.com/stomp");


const websocketExample = async ( ) => {
    const privateKey = await importPrivateKey(privateKeyBase64);
    const signature = await signPayload(privateKey, xKey);
  
    const base64Signature = Buffer.from(signature).toString("base64");
    const headers = {
      "x-key": testXkey,
      "x-signature": base64Signature,
    };
    client.connect(headers, websocketConnectCB, websocketErrorCB);
}

const websocketConnectCB = () => {
    client.subscribe("/topic/ETH_BTC.depth", (_data) => {
        // Data Recieved from Websocket
    });
}

const websocketErrorCB = () => console.log("Handle Error")


// Helper Methods

const importPrivateKey = async (_base64Private) => {
    const keyBuffer = Buffer.from(_base64Private, "base64");
    return await subtle.importKey(
      "pkcs8",
      keyBuffer,
      {
        name: "RSASSA-PKCS1-v1_5",
        hash: "SHA-256",
      },
      false,
      ["sign"]
    );
  };


  const signPayload = async (_privateKey, _signaturePayload) => {
    return await subtle.sign(
     {
       name: "RSASSA-PKCS1-v1_5",
       hash: "SHA-256",
     },
     _privateKey,
     Buffer.from(_signaturePayload)
   );
   }
