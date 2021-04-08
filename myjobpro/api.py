# -*- coding: utf-8 -*-
# Copyright (c) 2020, valiantsystems.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json, string, random
from frappe.utils import nowdate,cstr


@frappe.whitelist()
def update_role(doc,method):
	role=frappe.db.get_all('Has Role',fields=['*'],filters={'parent':doc.email,'role':'Candidate'})
	if not role:
		result= frappe.get_doc({
			"doctype": "Has Role",
			"name": nowdate(),
			"parent": doc.email,
			"parentfield": "roles",
			"parenttype": "User",
			"role": "Candidate"
			}).insert()

@frappe.whitelist(allow_guest=True)
def send_user_otp(mobile=None, user=None):
    try:
        '''Authenticate using otp.'''
        from frappe.twofactor import (should_run_2fa, authenticate_for_2factor,get_otpsecret_for_,
        confirm_otp_token, send_token_via_sms, send_token_via_email)
        import pyotp, os
        if mobile:
            user = frappe.db.get_value('User', {"mobile_no":mobile},'name')
        recipients = []
        recipients = recipients + mobile.split("\n") 
        recipients = list(set(recipients))
        otp_secret = get_otpsecret_for_(user)
        token = int(pyotp.TOTP(otp_secret).now())
        hotp = pyotp.HOTP(otp_secret)
        otp = hotp.at(int(token))
        frappe.log_error(otp, "userverification")
        # otp_issuer="INGC"
        message = 'Your verification code is {otp}'.format(otp=otp)
        status = send_sms(recipients, message)
        verification_obj = {
            'token_delivery': status,
            'prompt': status and 'Enter verification code sent to {}'.format(mobile[:4] + '******' + mobile[-3:]),
            "user": user,
            "tmp_id":token
        }
        return verification_obj
    except Exception as e:		
        frappe.log_error(frappe.get_traceback(), "myjobpro.api.send_user_otp")


@frappe.whitelist()
def send_sms(receiver_list, message):
    from frappe.core.doctype.sms_settings.sms_settings import send_sms
    if receiver_list and message:
        state = send_sms(receiver_list, cstr(message))
        return state


@frappe.whitelist(allow_guest=True)
def user_verification(otp=None, mobile=None, tmp_id=None, user=None):
    try:
        import pyotp, os
        from frappe.twofactor import get_otpsecret_for_
        if mobile:
            user = frappe.db.get_value('User', {"mobile_no":mobile},'name')
        otp_secret = get_otpsecret_for_(user)
        hotp = pyotp.HOTP(otp_secret)
        if tmp_id:
            if hotp.verify(otp, int(tmp_id)):
                return { 'status': 'success', 'user':user }
                # frappe.local.login_manager.login_as(user)
                # frappe.local.response['status'] = 'Success'
                # frappe.local.response['message'] = 'Logged In'
                # frappe.local.response["home_page"] = "/"
            else:
                return frappe.throw(_('Incorrect Verification code'), user)
    except Exception as e:		
        frappe.log_error(frappe.get_traceback(), "myjobpro.api.verify_user_otp")
        return { 'status':'failed' }