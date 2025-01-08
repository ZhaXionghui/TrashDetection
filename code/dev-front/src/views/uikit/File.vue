<script setup>
import ProductService from "@/service/ProductService";
import PhotoService from "@/service/PhotoService";
import { useLayout } from "@/layout/composables/layout";
import NodeService from "@/service/NodeService";
import { onMounted, ref, watch } from "vue";
import * as echarts from "echarts";
import {
  GridComponent,
  LegendComponent,
  MarkLineComponent,
  MarkPointComponent,
  TitleComponent,
  ToolboxComponent,
  TooltipComponent
} from "echarts/components";
import { LineChart } from "echarts/charts";
import { UniversalTransition } from "echarts/features";
import { CanvasRenderer } from "echarts/renderers";
import swal from "sweetalert";
import axios from "axios";

const { layoutConfig } = useLayout();
let documentStyle = getComputedStyle(document.documentElement);
let textColor = documentStyle.getPropertyValue("--text-color");
let textColorSecondary = documentStyle.getPropertyValue("--text-color-secondary");
let surfaceBorder = documentStyle.getPropertyValue("--surface-border");

const { isDarkTheme } = useLayout();
const products = ref([]);
const images = ref([]);
const lineOptions = ref(null);
const productService = new ProductService();
const photoService = new PhotoService();
const treeTableValue = ref(null);
const model1Value = ref(null);
const nodeService = new NodeService();
const lineData = ref(null);
const pieData = ref(null);
const polarData = ref(null);
const barData = ref(null);
const radarData = ref(null);

const pieOptions = ref(null);
const polarOptions = ref(null);
const barOptions = ref(null);
const radarOptions = ref(null);

const setColorOptions = () => {
  documentStyle = getComputedStyle(document.documentElement);
  textColor = documentStyle.getPropertyValue("--text-color");
  textColorSecondary = documentStyle.getPropertyValue("--text-color-secondary");
  surfaceBorder = documentStyle.getPropertyValue("--surface-border");
};
const setChart = () => {
  barData.value = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
      {
        label: "My First dataset",
        backgroundColor: documentStyle.getPropertyValue("--primary-500"),
        borderColor: documentStyle.getPropertyValue("--primary-500"),
        data: [65, 59, 80, 81, 56, 55, 40]
      },
      {
        label: "My Second dataset",
        backgroundColor: documentStyle.getPropertyValue("--primary-200"),
        borderColor: documentStyle.getPropertyValue("--primary-200"),
        data: [28, 48, 40, 19, 86, 27, 90]
      }
    ]
  };
  barOptions.value = {
    plugins: {
      legend: {
        labels: {
          fontColor: textColor
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: textColorSecondary,
          font: {
            weight: 500
          }
        },
        grid: {
          display: false,
          drawBorder: false
        }
      },
      y: {
        ticks: {
          color: textColorSecondary
        },
        grid: {
          color: surfaceBorder,
          drawBorder: false
        }
      }
    }
  };

  pieData.value = {
    labels: ["A", "B", "C"],
    datasets: [
      {
        data: [540, 325, 702],
        backgroundColor: [documentStyle.getPropertyValue("--indigo-500"), documentStyle.getPropertyValue("--purple-500"), documentStyle.getPropertyValue("--teal-500")],
        hoverBackgroundColor: [documentStyle.getPropertyValue("--indigo-400"), documentStyle.getPropertyValue("--purple-400"), documentStyle.getPropertyValue("--teal-400")]
      }
    ]
  };

  pieOptions.value = {
    plugins: {
      legend: {
        labels: {
          usePointStyle: true,
          color: textColor
        }
      }
    }
  };

  lineData.value = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
      {
        label: "First Dataset",
        data: [65, 59, 80, 81, 56, 55, 40],
        fill: false,
        backgroundColor: documentStyle.getPropertyValue("--primary-500"),
        borderColor: documentStyle.getPropertyValue("--primary-500"),
        tension: 0.4
      },
      {
        label: "Second Dataset",
        data: [28, 48, 40, 19, 86, 27, 90],
        fill: false,
        backgroundColor: documentStyle.getPropertyValue("--primary-200"),
        borderColor: documentStyle.getPropertyValue("--primary-200"),
        tension: 0.4
      }
    ]
  };

  lineOptions.value = {
    plugins: {
      legend: {
        labels: {
          fontColor: textColor
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: textColorSecondary
        },
        grid: {
          color: surfaceBorder,
          drawBorder: false
        }
      },
      y: {
        ticks: {
          color: textColorSecondary
        },
        grid: {
          color: surfaceBorder,
          drawBorder: false
        }
      }
    }
  };

  polarData.value = {
    datasets: [
      {
        data: [10, 16, 7, 3],
        backgroundColor: [documentStyle.getPropertyValue("--indigo-500"), documentStyle.getPropertyValue("--purple-500"), documentStyle.getPropertyValue("--teal-500"), documentStyle.getPropertyValue("--orange-500")],
        label: "My dataset"
      }
    ],
    labels: ["Indigo", "Purple", "Teal", "Orange"]
  };

  polarOptions.value = {
    plugins: {
      legend: {
        labels: {
          color: textColor
        }
      }
    },
    scales: {
      r: {
        grid: {
          color: surfaceBorder
        }
      }
    }
  };

  radarData.value = {
    labels: ["Eating", "Drinking", "Sleeping", "Designing", "Coding", "Cycling", "Running"],
    datasets: [
      {
        label: "My First dataset",
        borderColor: documentStyle.getPropertyValue("--indigo-400"),
        pointBackgroundColor: documentStyle.getPropertyValue("--indigo-400"),
        pointBorderColor: documentStyle.getPropertyValue("--indigo-400"),
        pointHoverBackgroundColor: textColor,
        pointHoverBorderColor: documentStyle.getPropertyValue("--indigo-400"),
        data: [65, 59, 90, 81, 56, 55, 40]
      },
      {
        label: "My Second dataset",
        borderColor: documentStyle.getPropertyValue("--purple-400"),
        pointBackgroundColor: documentStyle.getPropertyValue("--purple-400"),
        pointBorderColor: documentStyle.getPropertyValue("--purple-400"),
        pointHoverBackgroundColor: textColor,
        pointHoverBorderColor: documentStyle.getPropertyValue("--purple-400"),
        data: [28, 48, 40, 19, 96, 27, 100]
      }
    ]
  };

  radarOptions.value = {
    plugins: {
      legend: {
        labels: {
          fontColor: textColor
        }
      }
    },
    scales: {
      r: {
        grid: {
          color: textColorSecondary
        }
      }
    }
  };
};

const applyLightTheme = () => {
  lineOptions.value = {
    plugins: {
      legend: {
        labels: {
          color: "#495057"
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: "#495057"
        },
        grid: {
          color: "#ebedef"
        }
      },
      y: {
        ticks: {
          color: "#495057"
        },
        grid: {
          color: "#ebedef"
        }
      }
    }
  };
};
const applyDarkTheme = () => {
  lineOptions.value = {
    plugins: {
      legend: {
        labels: {
          color: "#ebedef"
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: "#ebedef"
        },
        grid: {
          color: "rgba(160, 167, 181, .3)"
        }
      },
      y: {
        ticks: {
          color: "#ebedef"
        },
        grid: {
          color: "rgba(160, 167, 181, .3)"
        }
      }
    }
  };
};

echarts.use([TitleComponent, ToolboxComponent, TooltipComponent, GridComponent, LegendComponent, MarkLineComponent, MarkPointComponent, LineChart, CanvasRenderer, UniversalTransition]);

onMounted(() => {
  productService.getProductsSmall().then((data) => (products.value = data));
  photoService.getImages().then((data) => (images.value = data));
  nodeService.getTreeTableNodes().then((data) => (treeTableValue.value = data));
  nodeService.getModel1Nodes().then((data) => (model1Value.value = data));
});

var read = function(name) {
  return JSON.parse(localStorage.getItem(name)); //把本地存储的my转成数组
};
// 在Vue3中，渲染完后执行函数
onMounted(() => {
  //调用需要执行的方法
  const ust = localStorage.getItem("ust");
  // console.log(ust);
  if (ust) {
    let usn = localStorage.getItem("usn");
    let st = localStorage.getItem("st");
    let et = localStorage.getItem("et");
    let ust = localStorage.getItem("ust");
    let uet = localStorage.getItem("uet");
    // console.log(usn);
    document.getElementById("Fan").innerHTML = "已选择的风机代号为：" + usn;
    document.getElementById("TimeRange").innerHTML = "对应的时间范围为：" + st + "~" + et;
    document.getElementById("UserTimeRange").innerHTML = "用户选择的时间范围为：" + ust + "~" + uet;
  }
});

watch(
  isDarkTheme,
  (val) => {
    if (val) {
      applyDarkTheme();
    } else {
      applyLightTheme();
    }
  },
  { immediate: true }
);

watch(
  layoutConfig.theme,
  () => {
    setColorOptions();
    setChart();
  },
  { immediate: true }
);

// var getBase64 = function(url, callback){
//   var Img = new Image(),
//     dataURL = '';
//   Img.src = url + '?v=' + Math.random();
//   Img.setAttribute('crossOrigin', 'Anonymous');
//   Img.onload = function () {
//     var canvas = document.createElement('canvas'),
//       width = Img.width,
//       height = Img.height;
//     canvas.width = width;
//     canvas.height = height;
//     canvas.getContext('2d').drawImage(Img, 0, 0, width, height);
//     dataURL = canvas.toDataURL('image/jpeg');
//     console.log(dataURL);
//     return callback ? callback(dataURL) : null;
//     // return dataURL.toString();
//     // console.log(dataURL);
//   };
// }

// function getBase64(url, callback) {
//     var Img = new Image(),
//         dataURL = '';
//     Img.src = url + '?v=' + Math.random();
//     Img.setAttribute('crossOrigin', 'Anonymous');
//     Img.onload = function () {
//         var canvas = document.createElement('canvas'),
//             width = Img.width,
//             height = Img.height;
//         canvas.width = width;
//         canvas.height = height;
//         canvas.getContext('2d').drawImage(Img, 0, 0, width, height);
//         dataURL = canvas.toDataURL('image/jpeg');
//         return callback ? callback(dataURL) : null;
//         console.log(dataURL);
//         // return dataURL.toString();
//         // console.log(dataURL);
//     };
// }


/**@url :图片服务器上的url
 * @img :图片url对应的图片
 * */
// const toBase64 = (img)=>{
//     const canvas = document.createElement('canvas'); //创建一个canvas元素
//     canvas.width = img.width; //把当前url对应的图片的宽度赋予canvas
//     canvas.height = img.height; //把当前url对应的图片的高度赋予canvas
//     const ctx = canvas.getContext('2d');
//     ctx.drawImage(img, 0, 0, canvas.width, canvas.height); //在画布上一比一的画出img
//     //调用canvas的toDataURL获取.jpg的base64数据
//   var dataURL = canvas.toDataURL('image/jpeg');
//     return dataURL;
//
// };
// const getImageUrlBase64 = (url) => {
//     const img = new Image();
//     img.crossOrigin = 'anonymous'; //处理跨域，后端也要设置跨域处理才行
//     img.src = url;
//     img.onload = () => {
//         return toBase64(img);
//     };
// };


// 第一个参数是图片的URL地址，第二个是转换成base64地址后要赋值给的img标签
// function getBase64Image (url) {
//   var image = new Image()
//   image.src = url + '?v=' + Math.random() // 处理缓存
//   image.crossOrigin = '*' // 支持跨域图片
//   image.onload = () => {
//     var base64 = drawBase64Image(image)
//     console.log(base64)
//     // this.$refs[ref].src = base64
//     return base64
//   }
// }
// function drawBase64Image (img) {
//   var canvas = document.createElement('canvas')
//   canvas.width = img.width
//   canvas.height = img.height
//   var ctx = canvas.getContext('2d')
//   ctx.drawImage(img, 0, 0, img.width, img.height)
//   var dataURL = canvas.toDataURL('image/png')
//   return dataURL
// }

// const coopCachetImg = ref([]);
// 发送请求到后端进行预测
const SampleTest = () => {
  const fj = selectedfj.value;
  function show(cfg) {
    swal({
      closeOnClickOutside: false,
      closeOnEsc: false,
      // 解构cfg对象，展开cfg对象所有属性
      ...cfg
    });
  }
  if (fj) {
    const method = fj.name;
    // 将url图片转为base64
    var imgURL = document.getElementById("imgsample").src;
    // 发送请求
    axios
      .post("http://39.104.62.62:5000/modelinfer", {
        method,
        imgURL
      })
      .then((res) => {
        const ret = res.data;
        console.log(ret);
        if (ret.code) {
          // 错误
          show({
            title: "错误",
            text: ret.data.msg,
            icon: "error",
            button: {
              text: "好的"
            }
          });
        } else {
          // 成功
          console.log(ret.data);
          const infer_img_url = "http://39.104.62.62:8877/" + ret.data.infer_img;
          const infer_json_url = "http://39.104.62.62:8877/" + ret.data.infer_json;
          const infer_img = document.getElementById("imgsample");
          console.log(infer_img_url);
          console.log(infer_json_url);
          infer_img.src = infer_img_url;
          // console.log(infer_img_url);
          // 读取url的json数据
          axios
            .get(infer_json_url)
            .then((res) => {
              const jsonStr = JSON.stringify(res.data);
              console.log(jsonStr);
              document.getElementById("Fan").innerHTML = "返回结果：" + jsonStr;
            })
            .catch((err) => {
              console.log(err);
            });
          // document.getElementById('Fan').innerHTML = '返回结果：' + jsonStr;

          // var save = function (name, arr) {
          //     localStorage.setItem(name, JSON.stringify(arr));
          // };
          // save("sysYD15",sysYD15)
          // var subtractedList = [];
          // for (var i = 0; i < oYD15.length; i++) {
          //     var diff = oYD15[i] - pYD15[i];
          //     subtractedList.push(Math.abs(diff));
          // }
        }
      })
      .catch((err) => {
        console.log(err);
      });
  } else {
    show({
      title: "错误",
      text: "请先选择推理模型",
      icon: "error",
      button: {
        text: "好的"
      }
    });
  }
};

// 提供给Dropdown组件使用的数据
const selectedfjs = ref([
  { name: "Picodet-xs", code: "1" },
  { name: "Picodet-s", code: "2" },
  { name: "PP-YOLO-Tiny", code: "3" },
  { name: "PP-YOLO-MobileNetV3-s", code: "4" },
  { name: "PP-YOLOE-crn-s", code: "5" },
  { name: "PP-YOLOE-crn-l", code: "6" },
  { name: "PP-YOLOE-plus-crn-s", code: "7" },
  { name: "PP-YOLOE-plus-crn-l", code: "8" },
  { name: "PP-YOLOv2", code: "9" },
  { name: "YOLOX-Tiny", code: "10" },
  { name: "YOLOX-cdn-Tiny", code: "11" },
  { name: "YOLOv8-n", code: "12" }
]);
const selectedfj = ref(null);

// 获取选择的风机代号，并打印
// const getSelectedfj = () => {
//   console.log(selectedfj.value);
//   // console.log(selectedfj.value.code);
// };

// 根据风机代号发送请求到后端获取数据信息
const Inference = () => {
  const fj = selectedfj.value;
  function show(cfg) {
    swal({
      closeOnClickOutside: false,
      closeOnEsc: false,
      // 解构cfg对象，展开cfg对象所有属性
      ...cfg
    });
  }
  if (fj) {
    const method = fj.name;
    // 发送请求
    axios
      .post("http://39.104.62.62:5000/Inference", {
        method
      })
      .then((res) => {
        const ret = res.data;
        console.log(ret);
        if (ret.code) {
          // 错误
          show({
            title: "错误",
            text: ret.data.msg,
            icon: "error",
            button: {
              text: "好的"
            }
          });
        } else {
          // 成功
          console.log(ret.data);
          const infer_img_url = "http://39.104.62.62:8877/" + ret.data.infer_img;
          const infer_json_url = "http://39.104.62.62:8877/" + ret.data.infer_json;
          const infer_img = document.getElementById("imgsample");
          console.log(infer_img_url);
          console.log(infer_json_url);
          infer_img.src = infer_img_url;
          // console.log(infer_img_url);
          // 读取url的json数据
          axios
            .get(infer_json_url)
            .then((res) => {
              const jsonStr = JSON.stringify(res.data);
              console.log(jsonStr);
              document.getElementById("Fan").innerHTML = "返回结果：" + jsonStr;
            })
            .catch((err) => {
              console.log(err);
            });
        }
      })
      .catch((err) => {
        console.log(err);
      });
  } else {
    show({
      title: "错误",
      text: "请先选择推理模型",
      icon: "error",
      button: {
        text: "好的"
      }
    });
  }
};


import { useToast } from "primevue/usetoast";
const toast = useToast();

const onUpload = () => {
  toast.add({ severity: "info", summary: "Success", detail: "File Uploaded", life: 3000 });
//
};

</script>

<template>
  <!--   添加div选择模型的选项-->
  <div class="fj-grid" id="Fj">
    <div class="card" id="FjSelect">
      <h5>模型选择</h5>
      <!--      使用main.js中的Dropdown来选择推理-->
      <!--令选择框和按钮居中-->
      <div class="p-d-flex p-jc-center">
        <Dropdown v-model="selectedfj" :options="selectedfjs" optionLabel="name"
                  placeholder="请选择一个推理模型"></Dropdown>
        <!--          令Dropdown与Button在同一行间存在少许间隙-->
        <br />
        <br />
<!--        <Button label="确定" @click="onSelect"></Button>-->
      </div>
    </div>
  </div>


  <div class="card">
    <h5>Samples</h5>
    <Carousel :value="products" :numVisible="1" :numScroll="1" :circular="false"
              :responsiveOptions="carouselResponsiveOptions">
      <template #item="product">
        <div class="product-item">
          <div class="product-item-content">
            <div class="mb-3">
              <Image :src="'http://39.104.62.62:8888/images/' + product.data.image" :alt="product.data.name" id="imgsample" class="product-image" />
<!--              <Image src='http://39.104.62.62:8888/images/000017.jpg' id="imgsample" class="product-image" preview />-->
            </div>
            <div>
              <div class="car-buttons mt-5">
                <Button type="button" class="p-button p-button-rounded mr-2" icon="pi pi-search" @click="SampleTest()"></Button>
                <!--<Button type="button" class="p-button-success p-button-rounded mr-2" icon="pi pi-star-fill"></Button>-->
                <!--<Button type="button" class="p-button-help p-button-rounded" icon="pi pi-cog"></Button>-->
              </div>
            </div>
          </div>
        </div>
      </template>
    </Carousel>
  </div>

<!--  <div class="product-item-content">-->
<!--    <div class="mb-3">-->
<!--      &lt;!&ndash;              <img :src="'http://39.104.62.62:8888/images/' + product.data.image" :alt="product.data.name"&ndash;&gt;-->
<!--      &lt;!&ndash;                   id="imgsample" class="product-image" />&ndash;&gt;-->
<!--      <Image src='http://39.104.62.62:8888/images/000017.jpg' id="imgsample" class="product-image" preview />-->
<!--    </div>-->
<!--    <div>-->
<!--      <div class="car-buttons mt-5">-->
<!--        <Button type="button" class="p-button p-button-rounded mr-2" icon="pi pi-search" @click="SampleTest()"></Button>-->
<!--        &lt;!&ndash;<Button type="button" class="p-button-success p-button-rounded mr-2" icon="pi pi-star-fill"></Button>&ndash;&gt;-->
<!--        &lt;!&ndash;<Button type="button" class="p-button-help p-button-rounded" icon="pi pi-cog"></Button>&ndash;&gt;-->
<!--      </div>-->
<!--    </div>-->
<!--  </div>-->
  <div class="grid p-fluid">
        <div class="col-12 md:col-12">
            <div class="card">
                <h5></h5>
                <Panel header="Results" :toggleable="true">
                    <p class="line-height-3 m-0" id="Fan">返回结果：</p>
                    <p></p>

                </Panel>

            </div>
          <Button label="开始推理" class="mr-2 mb-2" @click="Inference" />
        </div>
        <!-- 列表 -->
  </div>


    <div class="grid">
      <div class="col-12 md:col-12">
            <div class="card">
              <Toast />
                <h5>上传图片</h5>
                <FileUpload name="demo[]"
                            url="http://39.104.62.62:5000/Upload"
                            @uploader="onUpload()"
                            accept="image/*"
                            :multiple="false"
                            :maxFileSize="1000000"
                            id="uploadfile">
              <template #empty>
                <p>Drag and drop files to here to upload.</p>
              </template>
                <!-- <h5>Basic</h5>
        <FileUpload mode="basic" name="demo[]" accept="image/*" :maxFileSize="1000000" @uploader="onUpload" customUpload /> -->
              </FileUpload>
            </div>
      </div>
    </div>
</template>

<style lang="scss" scoped>
@import '@/assets/demo/styles/badges.scss';
@import '@/assets/demo/styles/items.scss';
</style>
