SET IDENTITY_INSERT PERSON ON
INSERT INTO [Person] ([Id],[Name],[Gender],[Birthday],[Age], [Alive], [Death], [Child], [Spouse])VALUES('I01','Joe Smith','M','1960-07-15','53','2013-12-31', 'NA', '{F23}')
SET IDENTITY_INSERT Person OFF
SET IDENTITY_INSERT Family ON
INSERT INTO [Family] ([Id],[Married],[Divorced],[Husband_ID],[Husband_Name],[Wife_ID],[Wife_Name], [Children])VALUES('F23','1980-02-14','NA','I01','Joe Smith','I07', 'Jennifer Smith', '{I26}, {I19}')
SET IDENTITY_INSERT Family OFF