<script setup>
import { ref, onMounted } from 'vue'

const pointX = ref(1);
const pointY = ref(1);
const elmX = ref(1);
const elmY = ref(1);

addEventListener("mousemove", 
  (event) => {
    pointX.value = event.clientX;
    pointY.value = event.clientY;
  }
);


onMounted(
  () => {
    const rect = document.body.querySelector(".vuenice").getBoundingClientRect();
    elmX.value = rect.x;
    elmY.value = rect.y;
  }
);

</script>

<template>
    <div class="vuenice" :style="{'--pointX':pointX, '--pointY':pointY, '--X':elmX, '--Y':elmY}">
        <p>hi mom</p>
        <button> click me</button>
    </div>
</template>

<style>
.vuenice {
    background-color: red;
    height: 6rem; 
    width: 6rem;

    transform: 
        perspective(500px)
        rotateX(min(max(calc(atan2(var(--pointY), var(--Y)) * 180 / 3.14159), 180deg), -180deg))
        rotateY(calc(atan2(var(--pointX), var(--X)) * 180 / 3.14159 * -1));
        
  transform-style: preserve-3d;
}
</style>