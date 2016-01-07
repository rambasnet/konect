txt_activation_msg = u'''Hey there {name},

                    To activate your  account, please copy/paste and load the following link to your browser
                    and follow the instruction.  Please note that activation link will expire in 48 hours.
                    If you didn't register for an account, you can safely ignore this email.

                    {link}.

                    Best,
                    {brand_name} Account Team
                    '''

html_activation_msg = '''Hey there {name}, <br /><br />

                    To activate your new account, please click on the following link.
                    Please note that activation link will expire in 48 hours. If you didn't register for an account,
                    you can safely ignore this email.<br /><br />

                    <a href="{link}" target="_blank">{link}</a>
                    <br /><br />

                    If clicking on the link doesn't work, please copy paste it to
                    your browser. <br /><br />

                    Best, <br />
                    {brand_name} Account Team
                    '''