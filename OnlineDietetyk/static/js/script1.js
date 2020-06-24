 //all htmls 
 $(document).ready(function(){
            $("#header").load("header.html");
        });

 //diet.html code
$(document).ready(function(){$('#searchMeal').click(function(){window.open('http://127.0.0.1:8000/OnlineDietetyk/diet_meals','_blank', 'width=400,height=500');return false;});})
$(document).ready(function(){$('#recalc').click(function(){RecalcTmpMeals(); });});
function RemoveTmpRow(tmpB){
            var tmpP=tmpB.parentNode.parentNode;
            tmpP.parentNode.removeChild(tmpP);
            }
function RecalcTmpMeals() {
            var tmpAllKcal = document.querySelectorAll("[class='tmpKcal']")
            var tmpAllProt = document.querySelectorAll("[class='tmpProt']")
            var tmpAllFat = document.querySelectorAll("[class='tmpFat']")
            var tmpAllCarbo = document.querySelectorAll("[class='tmpCarbo']")

            var tmpSumKcal = 0
            var tmpSumFat = 0
            var tmpSumCarbo = 0
            var tmpSumProt = 0

            for (var i=0;i<tmpAllKcal.length;i++){tmpSumKcal = tmpSumKcal + parseInt(tmpAllKcal[i].innerHTML)}
            for (var i=0;i<tmpAllProt.length;i++){tmpSumProt = tmpSumProt + parseInt(tmpAllProt[i].innerHTML)}
            for (var i=0;i<tmpAllFat.length;i++){tmpSumFat = tmpSumFat + parseInt(tmpAllFat[i].innerHTML)}
            for (var i=0;i<tmpAllCarbo.length;i++){tmpSumCarbo = tmpSumCarbo + parseInt(tmpAllCarbo[i].innerHTML)}

            $(".tmpSumKcal").html(tmpSumKcal);
            $(".tmpSumFat").html(tmpSumFat);
            $(".tmpSumCarbo").html(tmpSumCarbo);
            $(".tmpSumProt").html(tmpSumProt);
          }
$(document).ready(function(){$(".deleteCrossDiet").click(function(){
            $(this).toggleClass("hidden");
            $(this).next('form').toggleClass("hidden");
            $(this).next('form').find('.tmpID').attr('name','idMeal');
            });});
$(document).ready(function(){$(".removeMeal").click(function(){
            a1 = alert("Danie zostalo usunięty z dania.");
            url = $(location).attr('href')
            if(a1)
                {window.location.href = url;}});});
//diet_meals.html
$(document).ready(function(){$(".meal").click(function(){$(this).closest('tr').toggleClass("selected");});});
$(document).ready(function(){$(".meal").click(function(){AddMealName(); });});
function AddMealName() {
            var idMeal = parseInt($( "tr.selected").last()[0].id)
            var lastAddedName = $( ".selected .meal" ).last()[0].text
            var tmpAmount = parseInt($( ".selected .amount" ).last()[0].textContent)
            var tmpKcal = parseInt($( ".selected .kcal" ).last()[0].textContent)
            var tmpProt = parseInt($( ".selected .protein" ).last()[0].textContent)
            var tmpFat = parseInt($( ".selected .fat" ).last()[0].textContent)
            var tmpCarbo = parseInt($( ".selected .carbo" ).last()[0].textContent)

            window.opener.$("#list_of_meals").append("<tr> <td><input name='tmpDay' type='number'></td>" +
            "<td><select name='tmpTimeOfMeal'><option value = ''>Wybierz porę</option><option value = '1'>Śniadanie</option><option value = '2'>Drugie śniadanie</option><option value = '3'>" +
            "Obiad</option><option value = '4'>Podwieczorek</option><option value = '5'>Kolacja</option><option value = '6'>Przekąska</option><option value = '7'>Napój</option></select></td>" +
            "<td><select name='tmpMeal'><option value='"+ idMeal + "'>"+lastAddedName +
            "</option></select></td><td>" + tmpAmount + "</td>" +
            "<td><input type='number' name='tmpPortions' value='1'></td>" +
            "<td class='tmpKcal'>" + tmpKcal + "</td>" +
            "<td class='tmpProt'>" + tmpProt + "</td>" +
            "<td class='tmpFat'>" + tmpFat + "</td>" +
            "<td class='tmpCarbo'>" + tmpCarbo + "</td>" +
            "<td><button class='recalcMeal'>Przelicz po zmianie ilosci</button></td>" +
            "<td><input type='button' value='Usuń' class='removeMeal' onclick='RemoveTmpRow(this)'></td></tr>");
        }
//meal.html code
$(document).ready(function(){$('#searchProduct').click(function(){
	window.open('http://127.0.0.1:8000/OnlineDietetyk/meal_products','_blank', 'width=400,height=500');return false;
	});})

$(document).ready(function(){$("#saveProducts").click(function(){
            a1 = alert("Produkty zostaly dodane.");
            url = $(location).attr('href')
            if(a1)
                {window.location.href = url;}});});
$(document).ready(function(){$(".deleteCrossMeal").click(function(){
            $(this).toggleClass("hidden");
            $(this).next('form').toggleClass("hidden");
            $(this).next('form').find('.tmpID').attr('name','idProd');
        });});
$(document).ready(function(){$(".removeProduct").click(function(){
            a1 = alert("Produkty zostal usunięty z dania.");
            url = $(location).attr('href')
            if(a1)
                {window.location.href = url;}});});
//meal_products.html code
$(document).ready(function(){$(".product").click(function(){$(this).closest('tr').toggleClass("selected");});});
$(document).ready(function(){$(".product").click(function(){AddProductName(); });});
function AddProductName() {
            var idProduktu = parseInt($( "tr.selected").last()[0].id)
            var lastAddedName = $( ".selected .product" ).last()[0].text
            var tmpKcal = parseInt($( ".selected .kcal" ).last()[0].textContent)
            var sumKcal = parseInt(window.opener.$("#sumKcal").text())
            var tmpProt = parseInt($( ".selected .protein" ).last()[0].textContent)
            var sumProt = parseInt(window.opener.$("#sumProt").text())
            var tmpFat = parseInt($( ".selected .fat" ).last()[0].textContent)
            var sumFat = parseInt(window.opener.$("#sumFat").text())
            var tmpCarbo = parseInt($( ".selected .carbo" ).last()[0].textContent)
            var sumCarbo = parseInt(window.opener.$("#sumCarbo").text())
            var varNum = (window.opener.$("#list_of_products").children().length) + 1

            for (var i = 0; i < tmpKcal.length; i++) {
                sumKcal += tmpKcal[i] << 0;}
            window.opener.$("#list_of_products").append("<tr><td><input class='hidden' type='number' name='tmpProd' value='"+ idProduktu + "'><span>"+lastAddedName +
            "</span></td><td><input type='number' name='tmpAmount'><br /></td></tr>");
            window.opener.$("#sumKcal").html(sumKcal + tmpKcal);
            if (tmpFat) {
                window.opener.$("#sumFat").html(sumFat + tmpFat);}
            if (tmpProt) {
                window.opener.$("#sumProt").html(sumProt + tmpProt);}
            if (tmpCarbo) {
                window.opener.$("#sumCarbo").html(sumCarbo + tmpCarbo);}
        }


 //new_diet.html code
 $(document).ready(function(){$("#add_diet_button").click(function(){
			mandatory1 = $('#dietName')
			if (mandatory1.val()){
				a1 = alert("Dieta zostala dodana. Zostaniesz teraz przekierowany do strony konfiguracji diety.");
				if(a1)
					{window.location.reload();}
			}
            });});
//new_meal.html code
$(document).ready(function(){$("#add_meal_button").click(function(){
            a1 = alert("Danie zostalo dodana. Zostaniesz teraz przekierowany do strony konfiguracji dania.");
            if(a1)
                {window.location.reload();}});});
//new_product.html code
$(document).ready(function(){$("#add_product_button").click(function(){
            a1 = alert("Produkt zostala dodana. Zostaniesz teraz przekierowany do strony konfiguracji produktu.");
            if(a1)
                {window.location.reload();}});});
 // Patient.html code 
 $(document).ready(function(){$("#editData").click(function(){
            $(".savedData").toggleClass("hidden");
            $(".editData").toggleClass("hidden");
                });});
 $(document).ready(function(){$("#newVisit").click(function(){
            $("#tableVisits").append('<tr>' +
            '<td><input type="date" name="day"></td><td><input type="time" name="hour"></td>' +
            '<td><input type="checkbox" name="confirmed"></td><td><input type="checkbox" name="finished"></td>' +
            '<td><input type="submit" name="addVisit" value="Zapisz"></td></tr>');
                });});
 $(document).ready(function(){$("#updateVisit").click(function(){
            $(".id").toggleClass("hidden");
            $(".editData").toggleClass("hidden");
                });});
 $(document).ready(function(){$(".declineVisit").click(function(){
            $(this).closest("tr").find(".formTD").toggleClass("hidden");
            $(this).closest("tr").find(".controlTD").toggleClass("hidden");
            $(this).closest("tr").find('.idDeletedVisit').attr('name','visitToRemove');
                });});
 $(document).ready(function(){$(".declineVisitBack").click(function(){
            $(this).closest("tr").find(".formTD").toggleClass("hidden");
            $(this).closest("tr").find(".controlTD").toggleClass("hidden");
                });});
$(document).ready(function(){$(".updateVisit").click(function(){
            $(this).closest("tr").find(".visitItem").toggleClass("hidden");
            $(this).closest("tr").next("tr").toggleClass("hidden");
            $(this).closest("tr").next("tr").find('.idVisit').attr('name','visitToUpdate');
            $(this).closest("tr").next("tr").find('.newDate').attr('name','day');
            $(this).closest("tr").next("tr").find('.lastDay').attr('name','latestDay');
            $(this).closest("tr").next("tr").find('.newHour').attr('name','hour');
            $(this).closest("tr").next("tr").find('.lastHour').attr('name','latestHour');
            $(this).closest("tr").next("tr").find('.newConfirmation').attr('name','confirmed');
            $(this).closest("tr").next("tr").find('.newFinished').attr('name','finished');
                });});
$(document).ready(function(){$("#newTest").click(function(){
            $("#tableTests").append('<tr>' +
            '<td><input type="date" name="date"></td><' +
            '<td><input type="number" name="test1"></td><td><input type="number" name="test2"></td>' +
            '<td><input type="number" name="test3"></td><td><input type="submit" name="addTest" value="Zapisz"></td></tr>');
                });});
$(document).ready(function(){$(".declineTest").click(function(){
            $(this).closest("tr").find(".formTD").toggleClass("hidden");
            $(this).closest("tr").find(".controlTD").toggleClass("hidden");
            $(this).closest("tr").find('.idDeletedTest').attr('name','testToRemove');
                });});
$(document).ready(function(){$(".updateTest").click(function(){
            $(this).closest("tr").toggleClass("hidden");
            $(this).closest("tr").next("tr").toggleClass("hidden");
            $(this).closest("tr").next("tr").find('.idTest').attr('name','testToUpdate');
            $(this).closest("tr").next("tr").find('.newDate').attr('name','date');
            $(this).closest("tr").next("tr").find('.lastDate').attr('name','latestDate');
            $(this).closest("tr").next("tr").find('.newTest1').attr('name','test1');
            $(this).closest("tr").next("tr").find('.newTest2').attr('name','test2');
            $(this).closest("tr").next("tr").find('.newTest3').attr('name','test3');
                });});
$(document).ready(function(){$(".deleteDiet").click(function(){
            $(this).closest("tr").find(".formTD").toggleClass("hidden");
            $(this).closest("tr").find(".controlTD").toggleClass("hidden");
            $(this).closest("tr").find('.idDeletedDiet').attr('name','DietToRemove');
                });});
$(document).ready(function(){$(".updateDiet").click(function(){
            $(this).closest("tr").toggleClass("hidden");
            $(this).closest("tr").next("tr").toggleClass("hidden");
            $(this).closest("tr").next("tr").find('.idDiet').attr('name','dietToUpdate');
            $(this).closest("tr").next("tr").find('.newDate1').attr('name','date1');
            $(this).closest("tr").next("tr").find('.lastDate1').attr('name','latestDate1');
            $(this).closest("tr").next("tr").find('.newDate2').attr('name','date2');
            $(this).closest("tr").next("tr").find('.lastDate2').attr('name','latestDate2');
            $(this).closest("tr").next("tr").find('.newStatus').attr('name','status');
                });});
$(document).ready(function(){$("#newDiet").click(function(){window.open('http://127.0.0.1:8000/OnlineDietetyk/patient_diets','_blank', 'width=400,height=500');return false;});})

//patient_diets.html code
$(document).ready(function(){$(".diet").click(function(){$(this).closest('tr').toggleClass("selected");});});
$(document).ready(function(){$(".diet").click(function(){AddNewDietForm(); });});
function AddNewDietForm() {
            var idDiet = parseInt($( "tr.selected").last()[0].id)
            var nameDiet = $( ".selected .diet" ).last()[0].text
            window.opener.$("#tableDiets").append("<tr><td><select name='tmpDiet'><option value='"+ idDiet + "'>"+ nameDiet +
            "</option></select></td><td><input type='date' name='date1'><br /></td>" +
            "<td><input type='date' name='date2'><br /></td><td><input type='checkbox' name='status'></td>"+
            "<td><input type='submit' name='addDiet' class='glyphicon glyphicon-ok'><br />" +
            "<button class='glyphicon glyphicon-remove'></button></td></tr>");
        }
//product.html code
$(document).ready(function(){$("#edit_button").click(function()
		{$(".edit").toggleClass("hidden");
		 $(this).toggleClass("activeEdit");});});
$(document).ready(function(){$("#saved_button").click(function(){
            a1 = alert("zmiany zostaly zapisane");
            if(a1)
                {window.location.reload();}});});

//visits.html code
 $('.dropdown-toggle').dropdown()
$(document).ready(function(){$(".deleteCross").click(function(){
            $(this).toggleClass("hidden");
            $(this).next('form').toggleClass("hidden");
            $(this).next('form').find('.tmpID').attr('name','idVisit');
        });});
$(document).ready(function(){$(".declineVisit").click(function(){
            a1 = alert("Wizyta została odwołana");
            url = $(location).attr('href')
            if(a1)
                {window.location.href = url;}});});

			
//openfoodapi.html code
    $(document).ready(function(){$(".addProductAPI").click(function(){
            $(this).closest('tr').toggleClass("selected");
            $(this).toggleClass("hidden");
			$(this).closest('td').find('input').toggleClass("hidden");
        });});