/**
 * Nome do Autor: Jossian Brito
 * Data: 19/06/2026
 * Hora: 18:40
 * Versão: 1.1.0
 *
 * Histórico de Modificações:
 * - Removida a dependência externa 'node-fetch' para usar o fetch nativo global do Node 18+.
 * - Isso elimina a necessidade de um package.json e evita falhas de compilação (ZIP/Build) no Netlify.
 * - Adicionado tratamento de erro robusto com logs claros no console do Netlify.
 */

exports.handler = async function(event, context) {
    // Configura headers de resposta para garantir suporte CORS apropriado
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    };

    // Responde a requisições de preflight do CORS imediatamente
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers,
            body: ''
        };
    }

    // Aceita exclusivamente requisições do tipo POST para envio dos prompts
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            headers,
            body: JSON.stringify({ error: 'Método Não Permitido. Utilize POST.' })
        };
    }

    try {
        const { prompt, systemInstruction } = JSON.parse(event.body);

        if (!prompt) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ error: 'Falta o parâmetro essencial "prompt" no corpo da requisição.' })
            };
        }

        // Obtém a chave de API segura injetada na infraestrutura do Netlify
        const apiKey = process.env.GEMINI_API_KEY || "";

        if (!apiKey) {
            console.error('ERRO: Variável de ambiente GEMINI_API_KEY não foi encontrada.');
            return {
                statusCode: 500,
                headers,
                body: JSON.stringify({ 
                    error: 'Chave de API do Gemini não foi configurada no servidor Netlify.',
                    details: 'Por favor, registre a variável de ambiente GEMINI_API_KEY no painel de configurações do Netlify.'
                })
            };
        }

        // Modelo recomendado e suportado em ambiente de preview/produção do Canvas
        const modelName = process.env.GEMINI_MODEL || "gemini-2.5-flash";                  
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/${modelName}:generateContent?key=${apiKey}`;

        // Monta o payload conforme a estrutura oficial do ecossistema Gemini
        const payload = {
            contents: [
                {
                    parts: [
                        { text: prompt }
                    ]
                }
            ],
            systemInstruction: systemInstruction ? {
                parts: [
                    { text: systemInstruction }
                ]
            } : undefined
        };

        // Utiliza o fetch nativo global do Node.js, dispensando qualquer importação externa
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('ERRO na API do Gemini:', response.status, errorText);
            return {
                statusCode: response.status,
                headers,
                body: JSON.stringify({ 
                    error: `A API do Gemini retornou um erro inesperado: ${response.status}`,
                    details: errorText
                })
            };
        }

        const data = await response.json();
        
        // Extrai o conteúdo em texto retornado pela IA
        const textResult = data.candidates?.[0]?.content?.parts?.[0]?.text || "";

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({ text: textResult })
        };

    } catch (err) {
        console.error('Falha de processamento na função serverless:', err);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ 
                error: 'Falha interna na execução do Proxy Serverless.', 
                details: err.message 
            })
        };
    }
};