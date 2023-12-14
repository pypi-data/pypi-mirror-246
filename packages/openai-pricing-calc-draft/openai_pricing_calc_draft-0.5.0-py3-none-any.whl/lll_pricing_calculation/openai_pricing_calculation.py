import requests
embeddingsCategory='Embedding models'
embeddingsModel = 'Ada v2'
usageFieldName = "Usage"
inputFieldName = "Input"
outputFieldName = "Output"
thousand_constant = 1000
openai_api_pricing_url = 'https://openai-api-pricing-web-api.onrender.com/openai'

def calculate_openai_pricing(category, model,total_embedding_token_count,prompt_llm_token_count,completion_llm_token_count):
    pricingJson = get_api_pricing_data()
    return calculate_costs(pricingJson, category, model, total_embedding_token_count,prompt_llm_token_count,completion_llm_token_count)

def get_api_pricing_data():
    rawData = requests.get(openai_api_pricing_url)
    pricingJson = rawData.json()
    return pricingJson
    
def get_embeddings_data(pricingJson):
    return filter_pricing_data_by_model(pricingJson, embeddingsCategory,embeddingsModel)
    
def filter_pricing_data_by_model(pricingData, category, model):
    filteredData = {}
    for pricingCategory in pricingData:
        if pricingCategory == category:
            for item in pricingData[category]:
                if "Model" in item and item["Model"] == model:
                    filteredData[category] = [item]
    return filteredData 

def calculate_costs(pricingJson,category, model, total_embedding_token_count,prompt_llm_token_count,completion_llm_token_count):
    enginePricingData = filter_pricing_data_by_model(pricingJson, category, model)
    embeddingsModelPricing = get_embeddings_data(pricingJson)
    costForThousandCurrency,embeddingsCost = calculate_embeddings_token_price(embeddingsModelPricing,total_embedding_token_count)
    costForThousandCurrency,promptCost = calculate_prompt_token_price(enginePricingData,category,prompt_llm_token_count)
    costForThousandCurrency,completionTokenCost = calculate_completion_token_price(enginePricingData,category,completion_llm_token_count)
    total_cost = (embeddingsCost + promptCost + completionTokenCost)
    total_cost_rounded = round(total_cost,5)
    return costForThousandCurrency,embeddingsCost,promptCost,completionTokenCost,total_cost_rounded

# TODO - This function relies on a specific format. Pricing API page can include currency separately.
def getPricingInfo(priceText):
    currency = priceText[0]
    number = float(priceText[1:])
    return currency, number

def get_pricing_object(embeddingsModelPricing,embeddingsCategory,usageFieldName):
    if isinstance(embeddingsModelPricing[embeddingsCategory], list):
        pricing = embeddingsModelPricing[embeddingsCategory][0][usageFieldName]
    else:
        pricing = embeddingsModelPricing[embeddingsCategory][usageFieldName]
    return pricing

def calculate_embeddings_token_price(embeddingsModelPricing,total_embedding_token_count):
    costForThousandCurrency,costForThousandNumber = getPricingInfo(embeddingsModelPricing[embeddingsCategory][0][usageFieldName])
    calculated_cost = (total_embedding_token_count/thousand_constant) * costForThousandNumber
    calculated_cost_rounded = round(calculated_cost,5)
    return costForThousandCurrency,calculated_cost_rounded

def calculate_prompt_token_price(enginePricingData,category, total_prompt_token_count):
    costForThousandCurrency,costForThousandNumber = getPricingInfo(get_pricing_object(enginePricingData,category,inputFieldName))
    calculated_cost = (total_prompt_token_count/thousand_constant) * costForThousandNumber
    calculated_cost_rounded = round(calculated_cost,5)
    return costForThousandCurrency,calculated_cost_rounded

def calculate_completion_token_price(enginePricingData,category, total_completion_token_count):
    costForThousandCurrency,costForThousandNumber = getPricingInfo(get_pricing_object(enginePricingData,category,outputFieldName))
    # round the cost to 3rd decimal place
    calculated_cost = (total_completion_token_count/thousand_constant) * costForThousandNumber
    calculated_cost_rounded = round(calculated_cost,5)
    return costForThousandCurrency,calculated_cost_rounded