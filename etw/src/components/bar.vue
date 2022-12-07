<template>
    <div id="barMain">
        <div id="ctrlPanel">
            <div class="ctrlBlock">
                <el-radio-group v-model="type" size="small">
                    <el-radio label="0" border>按省</el-radio>
                    <el-radio label="1" border>按市</el-radio>
                </el-radio-group>
            </div>
            <div class="ctrlBlock">
                <el-select v-model="city" :disabled="typet" placeholder="Select" size="small" >
                    <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
            </div>
        </div>
        <div id="barViewport"></div>
    </div>
</template>
<script>
/* eslint-disable no-unused-vars,no-empty */
import * as d3 from 'd3';
import axios from 'axios';

export default {
    name: 'barView',
    data() {
        return {
            data: null,
            type: "0",
            typet: true,
            city: '上海',
            options: [],
        }
    },
    mounted() {
        // 获取数据
        axios.get('./旅游景点.json').then((res) => {
            var od = res.data;
            // 获取所有省
            for(let i = 0; i < od.length; i++)
                if(this.options.map((d) => {return d.value}).indexOf(od[i].divisions.split('/')[0]) == '-1')
                    this.options.push({value: od[i].divisions.split('/')[0], label: od[i].divisions.split('/')[0]});
            // 数据再处理
            var fd = [{}, {}];
            for(let i = 0; i < od.length; i++) {
                let p = od[i].divisions.split('/')[0];
                let c = od[i].divisions.split('/')[1];
                let l = od[i].level;
                if(p in fd[0]) {
                    if(l in fd[0][p]) {
                        fd[0][p][l] += 1;
                    } else {
                        fd[0][p][l] = 1;
                    }
                } else {
                    fd[0][p] = {};
                    fd[0][p][l] = 1;
                }
                if(p in fd[1]) {
                    if(c in fd[1][p]) {
                        if(l in fd[1][p][c]) {
                            fd[1][p][c][l] += 1;
                        } else {
                            fd[1][p][c][l] = 1;
                        }
                    } else {
                        fd[1][p][c] = {};
                        fd[1][p][c][l] = 1;
                    }
                } else {
                    fd[1][p] = {};
                    fd[1][p][c] = {};
                    fd[1][p][c][l] = 1;
                }
            }
            this.data = fd;
            console.log('bar', this.data)
            // 初始化
            this.init();
        })
    },
    methods: {
        init() {
            d3.select("#barViewport").selectAll("*").remove();
            const svg = d3.select("#barViewport").append("svg").attr("width", "100%").attr("height", "100%");
            const data = this.data;
            // 这里两个变量为用户交互选择的变量
            const city = this.city;
            const type = this.type;
            // 颜色
            const color = {
                "nan": "#FFFF99",
                "3A": "#7FC97F",
                "4A": "#FDC086",
                "5A": "#BEAED4",
            }
            // 根据模式不同选择不同数据
            if(type == '0') {
                draw(data[0])
            } else if (type == '1') {
                draw(data[1][city])
            }
            function draw(data) {
                const offset = [50, 50];
                const size = { w: 850, h: 300 };
                const barKeys = ['5A', '4A', '3A', 'nan'];
                // 图例
                let gLegend = svg.append('g');
                for(let i in barKeys) {
                    gLegend.append("rect")
                        .attr('x', 200 * i + 110)
                        .attr('y', 10)
                        .attr("width", 50)
                        .attr("height", 20)
                        .attr("fill", color[barKeys[i]]);
                    gLegend.append("text")
                        .text(barKeys[i])
                        .attr("font-size", 16)
                        .attr("font-weight", "bolder")
                        .attr("transform", `translate(${200 * i + 170}, 25)`);
                }
                // 获取最大值
                var maxAmount = 0;
                for(let i in data) {
                    let stack = 0;
                    for(let j in barKeys) {
                        if(barKeys[j] in data[i]) {
                            stack += data[i][barKeys[j]];
                        }
                    }
                    if(stack > maxAmount)
                        maxAmount = stack;
                }
                const keys = Object.keys(data);
                
                const rectWidth = size.w / keys.length - 2;
                // 比例尺
                const scaleY = d3.scaleLinear().domain([0, maxAmount * 1.1]).range([size.h, 0]);
                const scaleYr = d3.scaleLinear().domain([0, maxAmount * 1.1]).range([0, size.h]);
                const scaleX = d3.scaleBand().domain(keys).range([0, size.w]);
                // 坐标轴
                svg.append('g')
                    .call(d3.axisBottom(scaleX))
                    .attr("transform", `translate(${offset[0]}, ${offset[1] + size.h})`)
                        .selectAll("text")
                            .style("text-anchor", "end")
                            .attr("dx", "-.8em")
                            .attr("dy", ".15em")
                            .attr("transform", "rotate(-35)");
                svg.append('g')
                    .call(d3.axisLeft(scaleY))
                    .attr("transform", `translate(${offset[0]}, ${offset[1]})`)
                // 柱图
                for(let i in data) {
                    let x = scaleX(i) + offset[0] + 2;
                    let stack = 0;
                    for(let j in barKeys) {
                        if(barKeys[j] in data[i]) {
                            stack += data[i][barKeys[j]];
                            svg.append("rect")
                                .attr('x', x)
                                .attr('y', size.h - scaleYr(stack) + offset[1])
                                .attr('width', rectWidth)
                                .attr('height', scaleYr(data[i][barKeys[j]]))
                                .attr('fill', color[barKeys[j]]);
                        }
                    }
                }
            }
        },
    },
    watch: {
        type() {
            if(this.type == '1') this.typet = false;
            else if(this.type == '0') this.typet = true;
            this.init();
        },
        city() {
            this.init();
        }
    }
}
</script>
<style scoped>
#barMain {
    width: 100%;
    height: 100%;
    float: left;
    overflow: hidden;
    font-family: monospace;
    user-select: none;
    -moz-user-select: none;
    -webkit-user-select: none;
    -ms-user-select: none;
    /* background-color: aqua; */
}
#barViewport {
    width: 100%;
    height: calc(100% - 30px);
}
#ctrlPanel {
    width: 100%;
    height: 30px;
    padding: 5px;
}
.ctrlBlock {
    float: left;
    width: 50%;
    height: 100%;
}
</style>