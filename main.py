#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re


FORM = """
<style>
    .error{
        color:red;
    }
</style>
<h1>Signup</h1>
<form method="post">
    <table>
        <tbody>
            <tr>
                <td>
                    <label for="username">Username</label>
                </td>
                <td>
                    <input type="text" name="username" value="%(username)s">
                </td>
                <td>
                    <span class="error">%(error1)s</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="password">Password</label>
                </td>
                <td>
                    <input type="password" name="password" value="%(password)s">
                </td>
                <td>
                    <span class="error">%(error2)s</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="verify">Verify Password</label>
                </td>
                <td>
                    <input type="password" name="verify" value="%(verify)s">
                </td>
                <td>
                    <span class="error">%(error3)s</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="email">Email (optional)</label>
                </td>
                <td>
                    <input type="text" name="email" value="%(email)s">
                </td>
                <td>
                    <span class="error">%(error4)s</span>
                </td>
            <tr>
        </tbody>
    </table>
    <input type="submit">
    <input type="reset">
</form>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


def valid_username(username):
    return USER_RE.match(username)


def valid_password(password):
    return PASSWORD_RE.match(password)


def valid_email(email):
    return EMAIL_RE.match(email)


class MainHandler(webapp2.RequestHandler):
    def write_form(self, error1="", error2="", error3="", error4="",
                   username="", password="", verify="", email=""):
        self.response.out.write(FORM % {"error1": error1, "error2": error2,
                                        "error3": error3, "error4": error4,
                                        "username": username, "password": password,
                                        "verify": verify, "email": email})

    def get(self):
        self.write_form()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        have_error = False
        info_dict = {"username": username, "email": email}

        if not valid_username(username):
            have_error = True
            info_dict["error1"] = "That is not a valid username."
            info_dict["username"] = ""

        if not valid_password(password):
            have_error = True
            info_dict["error2"] = "That is not a valid password."

        if password != verify:
            have_error = True
            info_dict["error3"] = "Your passwords don't match."

        if (email != "") and (not valid_email(email)):
            have_error = True
            info_dict["error4"] = "That is not a valid email."
            info_dict["email"] = ""

        if have_error:
            self.write_form(**info_dict)
        else:
            escaped_username = cgi.escape(username, quote=True)
            self.redirect("/welcome?username=" + escaped_username)


class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        content = "<h1>Welcome, " + username + "!</h1>"
        self.response.out.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
