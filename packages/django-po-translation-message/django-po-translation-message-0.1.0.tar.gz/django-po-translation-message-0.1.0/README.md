# Python PO translation
## Description:
### _A package that will read key values and get the translated value from django.po file_

### Issue & Why the package is created:
### _I need to send English value and Arabic value to use it in a single page application. I searched for a package or tool to get the translated text from django.py file to use it in my SPA without duplicate the request and specify the language in the header in each request._

### _This package is useful for developers who need migrate from purly backend to have separated backend and front end and they want to send translated values from their backend to frontend without duplicate the request OR translate the same value in the front end and backend._

#### Steps:
``
python manage.py makemessages -l [your-language]
``
## Write the translation value in django.po file. Then
``
python manage.py compilemessages -l [your-language]
``

## License

MIT
