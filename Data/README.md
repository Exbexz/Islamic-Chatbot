## Database

There are 3 databases that stores different vector embedding according to their respoective feature extraction model<br>

model 1: google/canine-c <br>
model 2: malaysian-debartav-base<br>
model 3: multilingual-e5-large<br>

Both model 1 and 2 database have feature with size of 768 while model 3 have feature with size of 1024 <br>
Ensure that the model you used to convert question into vector will convert into the same size of those.<br>
If you wish to use other model you can use the model to create a new database first and you can use it in the app.py<br>
