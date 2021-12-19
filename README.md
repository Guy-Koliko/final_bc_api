## SECURING VOTING USING BLOCKCHAIN
This is the blockchain backend.<br> 
This part makes it possible for a user to send data to the blockchain via web interface.<br>
The backend has the blockchain side and a flask side. The purpose of the flask side is to<br>
link the html web interface to the blockchain so that data can be added to the BC.<br>
Also the flask enables us to create a usable API that can be parse by anyone who is authorize to use<br>
the data from the blockchain for a perticular purpose.

### CURRENT STATE OF THIS API
* FRONT END TO FOR THE BLOCKCHAIN
    ![front end to blockchain](front_end_for_blockchain.png)<br>
    This enables a user to communicate with the block system.<br>
    A user thus (EC officer) will have to enter all the available fields to send data to the BC system.<br><br>
* URL TO SEE DATA IN THE BLOCK
    ![url to see data in bc](url_to_see_data_in_bc.png)<br>
    With this URL the person handling the BC system can see the data in the BC.
    This same URL is what will be used by a developer to parse data from the BC.<br><br>

* URL TO MINE THE BC
    ![url to mine bc](url_to_mine_bc.png)<br>
    Before any data can be added to the BC it has to be mined.<br>
    This URL must be refresh to mine the data to the BC. We could allow auto refresh of that URL but due to memory issues we decided to do that manuelly.<br>

* URL TO CHECK DATA THAT ARE NOT MINE TO THE BC
    ![url to check data before mining](url_to_check_data_befor_mining.png)<br>
    The person handling the BC system can check for unmined data to the BC, and mine them if they like.
