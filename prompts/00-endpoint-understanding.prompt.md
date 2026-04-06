You are a MuleSoft integration architect.
 
Analyze ONE MuleSoft API endpoint and explain its behavior.
 
Rules:
-Analyze this MuleSoft code and create comprehensive documentation with, add file names along with starting and ending line numbers

1. **Main API endpoint XMl code** with Post method, \document api
2. **Complete flow and sub flows xml code** - trace ALL child flows, subflows, and processes recursively until the end
3. **Main API endpoint relevant RAML code** with Post method, \document api
4. **Main Api endpoint request and response Data Type Definition & Example RAML code** - trace Endpoint models and subflow defined transformation models
5. **All Datawave Transformation code from dwl files** (Original Endpoint, Subflows with their input/output formats)

- Do NOT convert code yet
- Focus only on this endpoint
- Identify request, response, transformations, dependencies, errors
- do not give me code block, just give me filenames with full path, line numbers.
 
 
Output:
 
1. **Endpoint Summary:**  
This endpoint handles POST requests to `/document` for uploading a document (such as a COVID case document) to AWS S3. It validates required headers, decodes the Base64 document, constructs the S3 key, uploads the file, and returns a JSON response with status, timestamp, and transaction ID. Errors are handled with standardized error responses.

---

2. **Final Response RAML file full paths:**  
   - c:\Tmp\Project Resources\sapi-project\aws-sapi-main\aws-sapi-main\src\main\resources\api\aws-sapi-types\aws-sapi-types.raml

---

3. **Endpoint details RAML file path and starting line number and ending line number:**  
   - c:\Tmp\Project aws-sapi.raml  
   - Starting Line Number: 17  
   - Ending Line Number: 45

---

4. **Show this section Request input RAML file path:**  
   - c:\Tmp\Project Resources\sapi-project\aws-sapi-main\aws-sapi-main\src\main\resources\api\aws-sapi-types\aws-sapi-types.raml

---

5. **Give me full path of Mule sub-flows called:**  
   - c:\Tmp\Project Resources\sapi-project\aws-sapi-main\aws-sapi-main\src\main\mule\implementations\upload-document-to-aws.xml  
   - c:\Tmp\Project Resources\sapi-project\aws-sapi-main\aws-sapi-main\src\main\mule\global-error-handler.xml  
   - (Referenced sub-flow: `global-prepare-error-response-sub-flow` in global-error-handler.xml)  
   - (Referenced sub-flow: `upload-s3-document` in upload-document-to-aws.xml, not shown in provided files but referenced)

---

6. **Give Related DataWeave scripts:**  
   - c:\Tmp\Project Resources\sapi-project\aws-sapi-main\aws-sapi-main\src\main\mule\implementations\upload-document-to-aws.xml (DataWeave transformations for decoding Base64 and setting response, lines 11-27, 29-38)
   - c:\Tmp\Project Resources\sapi-project\aws-sapi-main\aws-sapi-main\src\main\mule\global-error-handler.xml (DataWeave for error response, lines 180-204)

---

7. **Error scenarios:**  
   - 400 Bad Request: Returned for invalid input or validation errors.
   - 404 Not Found: Returned if the resource is not found.
   - 415 Unsupported Media Type: Returned if the request content type is not supported.
   - 500 Internal Server Error: Returned for unexpected errors during processing.
   - 503 Service Unavailable: Returned if S3 or an upstream service is unavailable.
   - Other HTTP and APIKIT errors as defined in global-error-handler.xml.

---

**Note:**  
- All line numbers and file paths are based on your provided files and selections.
- The endpoint depends on traits and types included from Exchange modules for header validation and error types.  
- The actual S3 upload logic is referenced via `upload-s3-document` sub-flow, which should be reviewed for full traceability if available.