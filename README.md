## Environment Setting

1. Use CMD
2. Import requirements.txt
3. Create virtual env
   * cd to current directory
   * enter 
    ```
    > virtualenv ven 
    > .\venv\Scripts\activate.bat
    ```
4. Set Flask 
    ```
    > set FLASK_APP=run.py
    > set FLASK_ENV=development
    ```
5. Create DB
   ```
    > flask db migrate
    > flask forge
    > flask run -h 140.xxx.xx.xx -p xxxx
   ```

6. Test Backend API service
   * Use Daimler_Based Distributed Mobility Service Internal API Document_v5.md
