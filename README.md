# cc510-chat
python code for kaist cc510 chat program (server , client)

# Notice
1. When you want to connect outside...
  - you need to open the firewall (or add new inbound rule if you are using Windows)
  - you need to add port forwarding rule to your AP if you are using it
  - And you have to change HOST IP address in 'configure.py' file (from '127.0.0.1' to your server IP address)
  
2. If you are using IDE(ex. PyCharm)
  - you may have trouble with the package import
  - Be sure that you have __init__.py file in your directory
  - And make your directory as a root of source (especially in PyCharm)
