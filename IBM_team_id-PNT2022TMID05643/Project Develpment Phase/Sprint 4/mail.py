import win32com.client
outlook = win32com.client.Dispatch('outlook application')
mail=outlook.CreateItem(0)
mail.To = 'kishorevijaykumar26@gmail.com'
mail.Subject = 'Need Plasma'
mail.Body = "Need Plasma of your blood group for: "
mail.send