<template>
    <div id="rankMain">
        <div class="rankBlock" id="rankLegend"></div>
        <div id="rankBars" v-infinite-scroll="loadMore"></div>
    </div>
</template>
<script>
/* eslint-disable no-unused-vars,no-empty */
import * as d3 from 'd3';
import axios from 'axios';

export default {
    name: 'rankView',
    data() {
        return {
            data: null,
            amount: 20, // 默认排多少个
            scale: null,
            offset: { x: 30, y: 30 },
            size: { w: 870, h: 30 },
            hasInit: false,
        }
    },
    mounted() {
        // 获取数据
        axios.get('./旅游景点.json').then((res) => {
            var d = res.data;
            // 排序
            d.sort(function(a, b){ return b.sales - a.sales });
            this.data = d;
            console.log('rank', this.data)
            // 初始化 绘制前20个
            this.init(0, this.amount);
        })
    },
    methods: {
        init(s, e) {
            const size = this.size;
            const offset = this.offset;
            const data = this.data;
            const scale = d3.scaleLinear().domain([0, this.getDomainMax(data[0].sales)]).range([0, size.w]);
            const div = d3.select("#rankBars");
            // 绘制坐标轴
            if(!this.hasInit) {
                const svgLegend = d3.select("#rankLegend").append("svg")
                    .attr("width", '100%')
                    .attr("height", '100%');
                this.scale = scale;
                svgLegend.append('g').call(d3.axisTop(scale))
                    .attr("transform", `translate(${offset.x}, ${offset.y})`)
                    .attr("font-size", 15);
            }
            // 绘制排名
            for(let i = s; i < e; i++) {
                var svg = div.append("div")
                    .attr("title", data[i].sales)
                    .attr("class", "rankBlock")
                    .style("width", "100%")
                    .style("height", "50px")
                    .append("svg")
                        .attr("width", "100%")
                        .attr("height", "100%");
                // 直方
                svg.append("rect")
                    .attr('x', offset.x)
                    .attr('y', offset.y - 30)
                    .attr("width", scale(data[i].sales))
                    .attr("height", size.h)
                    .attr("fill", "#3399ff");
                // 数据值
                svg.append("text")
                    .text(data[i].sales)
                    .attr("font-size", 16)
                    .attr("font-weight", "bolder")
                    .attr("transform", `translate(${offset.x + scale(data[i].sales) - String(data[i].sales).length * 10}, ${offset.y - size.h / 2 + 5})`);
                // 名称
                svg.append("text")
                    .text(data[i].name)
                    .attr("fill", "#99ff33")
                    .attr("font-weight", "bold")
                    .attr("font-size", 12)
                    .attr("transform", `translate(${offset.x + 4}, ${offset.y - size.h / 2 + 4})`);
                // 序号
                svg.append("text")
                    .text(i + 1)
                    .attr("font-size", 16)
                    .attr("font-weight", "bolder")
                    .attr("transform", `translate(${offset.x + - String(i + 1).length * 10 - 4}, ${offset.y - size.h / 2 + 5})`);
            }
            this.hasInit = true;
        },
        // 无限滚动依托
        loadMore() {
            if(this.hasInit) {
                this.amount += 5;
                this.init(this.amount - 5, this.amount)
            }
        },
        // 获取最大值并且向上取整
        getDomainMax(n) {
            let l, c = -1;
            while(n) {
                l = n % 10;
                n = parseInt(n / 10);
                c += 1;
            }
            return (l + 1) * 10 ** c
        }
    }
}
</script>
<style scoped>
#rankMain {
    width: 100%;
    height: 100%;
    float: left;
    overflow: hidden;
    font-family: monospace;
    /* background-color: chartreuse; */
}
#rankBars {
    width: 100%;
    height: 100%;
    float: left;
    overflow: auto;
}
#rankBars::-webkit-scrollbar {
  width: 5px;     
  height: 5px;
  scrollbar-arrow-color:red;
}
#rankBars::-webkit-scrollbar-thumb {
  border-radius: 5px;
  box-shadow: inset 0 0 10px rgba(0,0,0,0.3);
  background: rgba(255,255,255,0.3);
  scrollbar-arrow-color:red;
}
#rankBars::-webkit-scrollbar-track { 
  box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
  border-radius: 0;
  background: rgba(0,0,0,0.1);
}
.rankBlock {
    width: 100%;
    height: 50px;
}
</style>