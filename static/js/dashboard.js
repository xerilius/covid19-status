"use strict";
$(document).ready(function() {

    const countyLinks = document.getElementsByClassName("sidenav__list-item");
    for (let countyLink of countyLinks) {
        countyLink.addEventListener('click', showCountyInfo);
    }
 
    function showCountyInfo(evt) {
        const countyLink = evt.target;
        const countyId = countyLink.dataset.countyId;
        console.log(countyLink);
           // Grab json data
        d3.queue()
        .defer(d3.json, `/data/${countyId}`)
        .await(function(error) {
            if (error) throw error;
            console.log("Goodbye!");
          });

        let data = dataset['data'];
        // console.log(dataset)
        
        let time_parse = d3.timeParse("%Y-%m-%d");
        let time_format = d3.timeFormat("%Y-%m-%d");
        let margin = {top: 25, right: 0, bottom: 25, left: 0}
        let c_width = 1000;
        let c_height = 800;
        let padding = 50;
        
        // convert date into date object
        data.forEach(function(e, i) {
            data[i].date = time_parse(e.date);
        });

        // scales
        let x_scale = d3.scaleTime()
            .domain([
                d3.min(data, function(d) {
                    return d.date;
                }),
                d3.max(data, function(d) {
                    return d.date;
                })
            ])
            .range([padding, c_width - padding]);

        let y_scale = d3.scaleLinear()
            .domain([
                0, d3.max(data, function(d) {
                    return d.num;
                })
            ])
            .range([c_height - padding, padding]);

        //  SVG element
        let svg = d3.select("#confirmed-graph")
            .append("svg")
            .attr("width", c_width)
            .attr("height", c_height);

        // Create Axes
        let x_axis = d3.axisBottom(x_scale)
            .ticks(10)
            .tickFormat(time_format);
        let y_axis = d3.axisLeft(y_scale)
            .ticks(12);

        // Drawing and positioning axes
        svg.append("g")
            .attr("transform", "translate(0," + (c_height - padding) + ")")
            .call(x_axis);

        // Text label for x-axis
        svg.append("text")
            .attr("x", (c_width/2) )
            .attr("y", 790 )
            .style("text-anchor", "middle")
            .text("Date");

        svg.append("g")
            .attr("transform", "translate(" + padding + ",0)")
            .call(y_axis);
        // Text label for y-axis
        svg.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 0-margin.left)
            .attr("x", 0-(c_height/2))
            .attr("dy", "1em")
            .style("text-anchor", "middle")
            .text("Confirmed");
        
        // Create line on Graph
        let line = d3.line() // will return another function that generates line
            .x(function(d){
                return x_scale(d.date);
            })
            .y(function(d){
                return y_scale(d.num);
            });

        //  line can only be used with path element, since data return is only compatable with path el
        svg.append('path') // a line is one continous path
            .datum(data) // datum binds all data to 'path' element all at once
            .attr('fill', 'none')
            .attr('stroke', 'black')
            .attr('stroke-width', 2)
            .attr('d', line); //set d attr to line funct
        

    }


    const getDate = function() {
        const now = new Date(); 
        const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        const weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        
        let mth = months[now.getMonth()];
        let dates = now.getDate();
        let year = now.getFullYear();
        let weekday = weekdays[now.getDay()];
        let todaysDate = mth + " " + dates + ", " + year + " (" + weekday + ")";
        // Display on page
        $(".header__date").html(todaysDate);
    }
    getDate()

    const getTime = function() {
        const now = new Date();
        let timeOfDay = "AM";
        let hours = now.getHours();
        if (hours > 12) {
            hours = hours - 12;
            timeOfDay = " PM";
        }
        let minutes = now.getMinutes();
        if (minutes < 10) {
            minutes = "0" + minutes.toString()
        }
        let seconds = now.getSeconds();
        if (seconds < 10) {
            seconds = "0" + seconds.toString()
        }
        let todaysTime = hours.toString() + " : " + minutes.toString() + " : " + seconds.toString() + " " + timeOfDay;
        $(".main-header__time").text(todaysTime);        
    }
    setInterval(getTime, 1000);

});