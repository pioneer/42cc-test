from windmill.authoring import WindmillTestClient
from django.conf import settings
from common.forms import UserForm

client = WindmillTestClient(__name__)

client.open(url=u'http://localhost:8000/logout/')
client.waits.forPageLoad(timeout=u'20000')
client.open(url=u'http://localhost:8000/login/')
client.waits.forPageLoad(timeout=u'20000')
client.waits.forElement(timeout=u'8000', id=u'id_username')
client.type(text=u'pioneer', id=u'id_username')
client.type(text=u'123456', id=u'id_password')
client.click(value=u'Login')
client.waits.forPageLoad(timeout=u'20000')
client.click(link=u'Edit this info')
client.waits.forPageLoad(timeout=u'20000')
client.waits.forElement(timeout=u'8000', id=u'id_birthdate')
client.click(id=u'id_birthdate')
client.waits.forElement(xpath=u"//div[@id='ui-datepicker-div']", \
                        timeout=u'8000')
client.click(link=u'24')
client.click(value=u'Save')
FORM_CONTROL_IDS = ["id_%s" % field_name for field_name in \
                    UserForm._meta.fields] + ["id_submit"]
for id in FORM_CONTROL_IDS:
    client.asserts.assertNode(jquery=u'("#%s:disabled")[0]' % id)
client.asserts.assertNode(jquery=u'("#ajax_loader:visible")[0]')
client.waits.sleep(milliseconds=u'%s' % \
                   ((settings.AJAX_FORM_COUNTDOWN_TIME-5) * 1000))
for id in FORM_CONTROL_IDS:
    client.asserts.assertNode(jquery=u'("#%s:enabled")[0]' % id)
client.asserts.assertNode(jquery=u'("#ajax_loader:hidden")[0]')
client.click(link=u'View this info')
client.waits.forPageLoad(timeout=u'20000')
client.asserts.assertText(validator=u'24 Jun 1980', id=u'birthdate')

# Roll back to initial data
client.open(url=u'http://localhost:8000/form/')
client.waits.forPageLoad(timeout=u'20000')
client.waits.forElement(timeout=u'8000', id=u'id_birthdate')
client.type(text=u'1980-06-15', id=u'id_birthdate')
client.click(value=u'Save')
client.waits.sleep(milliseconds=u'%s' % \
                   ((settings.AJAX_FORM_COUNTDOWN_TIME + 1) * 1000))
client.click(link=u'View this info')
client.waits.forPageLoad(timeout=u'20000')
client.asserts.assertText(validator=u'15 Jun 1980', id=u'birthdate')
