<template>
    <div class="form-group">
        <label :for="id">{{ label }}</label>
        <input 
            :type="type" 
            :id="id" 
            :placeholder="placeholder" 
            :value="modelValue" 
            @input="$emit('update:modelValue', $event.target.value)" 
        />
    </div>
</template>

<script>
export default {
    props: {
        label: String,
        type: { type: String, default: 'text' },
        id: String,
        placeholder: String,
        modelValue: String,
    },
};
</script>

<style scoped>
.form-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 15px;
}

label {
    font-size: 14px;
    font-weight: 500;
    color: #666;
    margin-bottom: 8px;
}

input {
    font-size: 16px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
    outline: none;
    transition: border-color 0.3s;
}

input:focus {
    border-color: #333;
}
</style>
