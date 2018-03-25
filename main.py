import zomatoc
import csv


config={
  "user_key":"ZOMATO_API_KEY"
}
    
zomato = zomatoc.initialize_app(config)

s="Yes"
clist = []
while(s!="No"):
	s=input("\nEnter city: ")
	if(s!="No"):
		clist.append(s)
for ci in clist:
	cid=zomato.get_city_ID(ci);
	if(cid!=0):
		st=0

		filename=ci+".csv"

		with open(filename, 'w', newline='') as csvfile:
			fieldnames = ['name', 'average_cost_for_two']
			writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
			writer.writeheader()
			while(st<=81):
				restaurant_list = zomato.restaurant_search(cityid=cid,start=st)
				print(type(restaurant_list))
				print(restaurant_list)
				writer.writerows(restaurant_list)
				print("Done")
				st=st+20




