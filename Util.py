import ipaddress

class Util:
    def validate_ip_address(self,address):
        try:
            self.ip = ipaddress.ip_address(address)
            return True
        except ValueError:
            return False 

    def validate_date(self,date):
        try:
            day,month,year=date.split('/')
        except:
            return False
        else:
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

            if int(day) > 0 and int(day) <= 31:
                    if month.capitalize() in months:
                        if len(year) == 4:
                            return True
            return False

