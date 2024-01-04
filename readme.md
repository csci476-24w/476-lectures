% CSCI 476 / 576 Lecture Notebooks
% Winter 2024

## Overview

This repository hosts the notebooks and in-class codebase for the lectures in CSCI 476 / 576. I'll be running it remotely from a lab machine; I recommend you do the same to ensure that versioning and packages are all the same.

## Setup

1. Clone the repository.

2. Create and activate a virtualenv:

   ```
   $ python3 -m venv 476env
   $ source 476env/bin/activate
   ```

3. Install the required python packages:

   ```
   $ pip install -r requirements.txt
   ```

4. If running locally, launch jupyterlab:

   ```
   jupyter lab
   ```

   and use the Jupyterlab interface to navigate around among notebooks and code files.

   If you wish to run on a lab machine, to ensure software compatibility and versioning hapiness, follow the instructions in the next section to remotely access a lab machine, launch JupyterLab, and connect to the server through an SSH tunnel. Note that if you're running the server on a remote machine, you should of course complete steps 1-3 above on the remote host.

## Running JupyterLab Remotely - Setup

0. **Set up VPN.** Follow the instructions [here](https://support.cs.wwu.edu/home/access/index.html) to set up a VPN client and connect to the VPN. You should be able to use either the CS VPN or the University-wide WWU VPN. If using the WWU VPN, I recommend connecting using the **Split Tunnel** option - this way only network traffic destined for the `wwu.edu` domain will flow through Western. The CS VPN is automatically set up as a split tunnel.

1. **Set up your SSH config.** Follow the instructions on the CS Support Wiki [here](https://gitlab.cs.wwu.edu/cs-support/public/-/wikis/home/survival_guide/day_to_day/Remotely_Accessing_Resources#ssh-config-file-suggestions-based-on-the-above) to ensure that your **local machine**'s SSH config file is set up to access CS labs via the jump server. In particular, make sure you have the sections that define the **csjump** host and the **cf???-???** host. The [SSH config file recommended by CS Support](https://support.cs.wwu.edu/home/survival_guide/day_to_day/Remotely_Accessing_Resources.html#bsd-linux-macos-sample-config-file) contains the following; don't forget to replace ${username} with your CS username:

```
Host csjump
  Hostname jump.cs.wwu.edu
  Port 922
  User ${username}
  ForwardX11 yes
  ForwardX11Trusted yes

Host cf???-??
  HostName %h.cs.wwu.edu
  Port 922
  User ${username}
  ForwardX11 yes
  ForwardX11Trusted yes
  ProxyJump csjump
```
2. **Get a jupyter notebook server running on a remote lab machine.** *Note: I strongly recommend against using VS Code for any of these steps, even if you've used it before; it is unnecessary and only complicates things for our purposes.* Open a terminal on your local machine and use `ssh` to connect to a lab machine of your choice by selecting a room number and machine number.  A list of such systems can be found on the [CS Support Wiki](https://gitlab.cs.wwu.edu/cs-support/public/-/wikis/home/survival_guide/day_to_day/Remotely_Accessing_Resources#systems-for-remote-access-only-new-for-fall-2021).

   With the above config file set up, you can SSH to a lab machine of your choice using a command such as:
   
   ````
   ssh cfRRR-MM
   ````
   
   where `RRR` should be replaced by a room number (e.g., `405`) and `MM` should be replaced by a machine number (e.g., `04`). Once you're there, navigate to the root directory of this repository and then start a JupyterLab server using the following command, using a 4-digit port number of your choice in place of `PPPP`:

    ```
    jupyter lab --no-browser --port=PPPP
    ```
   This command needs to stay running in order to keep the server running, so you should leave this terminal window alone as long as you need to access the server. To quit the server when you're done working, press Ctrl-C then enter "y" at the prompt, or press Ctrl-C twice in a row, to shut down the server.
3. **Set up a tunnel.** Fortunately but inconveniently, our lab machines are not directly accessible from the internet, so we can't just point our browser at the server and connect. Instead, we'll set up an **ssh tunnel**. This effectively takes any internet traffic going to a particular port on your local machine and transparently sends it off to the remote machine, over a secure SSH connection. In this case, we're make it seem as though the notebook server is running locally, and in the background send all the traffic over to the remote lab machine. On your **local machine**, open up a new terminal (separate from the one you used in step 2) and run the following command (replace `PPPP`, `RRR`, and `MM` as before):

   ```
   ssh -NL PPPP:localhost:PPPP cfRRR-MM
   ```
This command needs to stay running in order to keep the tunnel open; on entering the command, you should just see no output and no new prompt for another command. You should leave theis terminal window open with this command running as long as you need to access the server. To close the tunnel when you're done accessing the notebook server, you can press Ctrl-c and you should be back to a shell prompt.
4. **Connect to the server using a browser.** Finally, go back to the terminal where you started the Jupyter server. Among the output, you should see something like the following:

   ```
       To access the notebook, open this file in a browser:
           file:///home/wehrwes/.local/share/jupyter/runtime/nbserver-11514-open.html
       Or copy and paste one of these URLs:
           http://localhost:8888/?token=c303308678e757fd3a1dd1dedab3043ff52111964e2f831b
        or http://127.0.0.1:8888/?token=c303308678e757fd3a1dd1dedab3043ff52111964e2f831b
   ```

   Copy and paste the URL into your browser as directed, and you should be greeted with a functioning Jupyter notebook session.

## Per-Session Remote Access

Once you've completed the above, you should be able to begin a session to work on Jupyter with the following steps:

1. Connect to VPN.
2. Set up a tunnel `ssh -NL PPPP:localhost:PPPP cfRRR-MM` (on your local machine)
3. SSH to the lab machine `ssh cfRRR-MM` (from your local machine) and go to this repo's root directory.
4. Activate your virtualenv: `source 476env/bin/activate`
5. Start the server: `jupyter lab --no-browser --port=PPPP` (on the remote machine)
6. Connect to the server through your browser (on your local machine) by pasting the URL given when the server starts.

To end your session:

1. Save your notebook if needed, and close the browser window 
2. Shut down the notebook server on the remote machine by pressing Ctrl-c twice in the terminal window where you started it (on the remote machine).
3. Close the SSH connection to the remote machine by typing `exit` or pressing Ctrl-d.
4. Close the SSH tunnel by pressing Ctrl-c in the terminal window where you opened it (on your local machine).

## Troubleshooting

**Problem:** when trying to open the SSH tunnel, you see a message like this:

```
$ ssh -NL 8888:localhost:8888 cf162-08
bind [127.0.0.1]:8888: Address already in use
channel_setup_fwd_listener_tcpip: cannot listen to port: 8888
Could not request local forwarding.
```

This error message happens because you already have a notebook server running, occupying the requested port on your **local** computer. In this case, I was running a local server on port 8888 (the default), and tried to tunnel the same port to cf162-08. The solution is to either shut down the local server or pick a different 4-digit port number.

---

**Problem:** when trying to connect to the URL given when the server starts, you receive an "Unable to connect" error in your browser. 

This is happening because the server started successfully, but the SSH tunnel is not in place. This might be because:

*  The SSH tunnel hasn't been created because you forgot to run `ssh -NL PPPP:localhost:PPPP cfRRR-MM` on your local machine.

* The port you chose when starting the server (`--port=PPPP`) was in use, so the notebook server started on a different port. If you look at the server's startup message, it might say something like:

  ```
  [I 15:54:37.696 NotebookApp] The port 8668 is already in use, trying another port.
  ```

  In this case, you'll notice that the server URL looks like `localhost:PPPP`, where the server has chosen a different port than you specified; in my case, I asked for `8668` but that was in use so it used `8669` instead. To fix this, simply Ctrl-C to cancel the SSH tunnel command that you ran, and re-run it with the correct port number (in my example, `ssh -NL 8669 localhost:8669 cfRRR-MM`). Then, you should be able to reload your browser window and be connected to the notebook server as intended.
