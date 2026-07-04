<template>
  <div class="homepage-wrapper">
    <!-- Transparent Sticky Navbar -->
    <Navbar />

    <!-- Full-Screen Hero Section -->
    <Hero />

    <!-- 4 Premium Feature Cards -->
    <Features />

    <!-- Popular Treks Grid -->
    <PopularTreks />

    <!-- Alternating Details Section (Why Choose Us) -->
    <WhyChooseUs />

    <!-- Counter Statistics -->
    <Statistics />

    <!-- Reviewer Testimonials Slider -->
    <Testimonials />

    <!-- Masonry Image Scrapbook -->
    <Gallery />

    <!-- Signup CTA -->
    <CallToAction />

    <!-- Deep Green Footer -->
    <Footer />
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'
import Hero from '../components/Hero.vue'
import Features from '../components/Features.vue'
import WhyChooseUs from '../components/WhyChooseUs.vue'
import PopularTreks from '../components/PopularTreks.vue'
import Statistics from '../components/Statistics.vue'
import Testimonials from '../components/Testimonials.vue'
import Gallery from '../components/Gallery.vue'
import CallToAction from '../components/CallToAction.vue'
import Footer from '../components/Footer.vue'
import { onMounted } from "vue";
import api from "../api/api";

onMounted(async () => {
  try {
    const response = await api.get("/test");
    console.log(response.data);
  } catch (err) {
    console.error(err);
  }
});
</script>

<style scoped>
.homepage-wrapper {
  position: relative;
  width: 100%;
}
</style>


