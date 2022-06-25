# LeanTechTest
### Author: Juan Martin Uribe
## User Manual
Using a virtual evironment install the requirements located at the US-CA-FuelTaxRates directory
`$ pip install -r requirements.txt`

Run the main file, `python .\CurrentFuelRates.py `

The class `CurrentFuelRates` opens a chromium connection with the https://www.iftach.org/taxmatrix4/Taxmatrix.php web page when intialized.
In order to get the fuel tax prices, call the `getRates()` method of the created instance, this method returns a list.

Finally, the `sendEmail()` method sends the tabulated rates as a html file and the python source code. It receives the message and name of file as a parameter.

### Troubleshoot

In case something stops working, check the most likely causes of the issue:
#### Table indexes and id:
The table indexes and id of the `tr` tag html element located at the web page are constants declared in the `getRates()` method:

        STATE_INDEX = 1
        SPECIAL_DIESEL_RATE_INDEX,BIODIESEL_RATE_INDEX = 4,14
        TABLE_ID = "rwd-table-large"
Check the source html code to verify that they have not been modified due to the importance of these indexes to locate the elements

If you want to add any other row, check the index and add it.

#### Email info and server:
The email is located in the `sendEmail()` method, check that it is the desired email.
As for the password, the smtp server only works with encrypted application password, look for it in the security settings of your email office.

The last common issue that could cause problems is the server address, it is currently working with `smtp.gmail.com` so look for another available service in case it does not work or want another.
