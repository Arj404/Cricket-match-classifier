import os 
  
# Function to rename multiple files 
def main(): 
  
    for count, filename in enumerate(os.listdir("review")): 
        dst =str(count) + ".jpg"
        src ='review/'+ filename 
        dst ='review/'+ dst 
          
        # rename() function will 
        # rename all the files 
        os.rename(src, dst) 
  
# Driver Code 
if __name__ == '__main__': 
      
    # Calling main() function 
    main() 