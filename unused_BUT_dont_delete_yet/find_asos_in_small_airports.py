def TRW(request):
    if request.method == "POST":
        beg_url = 'https://www.aviationweather.gov/metar/data?ids='
        end_url = '&format=raw&hours=0&taf=off&layout=on&date=0'
        print("############     running     ###############")
        places = Airfield.objects.all()
        count = 4000
        stop = 5000
        index = 0
        for each in places:
            if index > count and index < stop:
                temp = each.identifier
                tempp = list(temp)
                if tempp[0] != 'K':
                    AI = temp
                    print(AI, "   ", end="")
                    url = beg_url + AI + end_url
                    res = requests.get(url)
                    text = res.text
                    find_beg = "<!-- Data starts here -->"
                    find_end = "<br /><hr"
                    beg_position_of_data = text.find(find_beg) + 25
                    end_position_of_data = text.find(find_end)
                    if "No METAR found" not in text[beg_position_of_data:end_position_of_data]:
                        print("FOUND ONE !!!!", text[beg_position_of_data:end_position_of_data])
            index += 1
    return render(request, 'clearskies_app/plan.html', {})
