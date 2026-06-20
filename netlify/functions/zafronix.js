/**
 * Nome do Autor: Jossian Brito
 * Data: 19/06/2026
 * Versão: 1.0.0
 *
 * Proxy serverless para a Zafronix World Cup API (https://api.zafronix.com).
 * - Mantém a ZAFRONIX_API_KEY exclusivamente no servidor (nunca exposta ao cliente).
 * - Usado apenas para dados HISTÓRICOS/estáticos (1930–2022), que cabem no plano free.
 *   O ao vivo da Copa 2026 continua vindo da worldcup26.ir (live é pago na Zafronix).
 * - Usa o fetch nativo do Node 18+ (sem dependências externas, evita falha de build no Netlify).
 */

const API_BASE = 'https://api.zafronix.com/fifa/worldcup/v1';

// Allowlist de prefixos de endpoint para evitar SSRF/uso indevido do proxy.
const ALLOWED_PREFIXES = [
    '/tournaments',
    '/teams',
    '/players',
    '/venues',
    '/trivia',
    '/compare',
    '/aggregates'
];

exports.handler = async function(event) {
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Content-Type': 'application/json',
        // Cache no CDN do Netlify para respeitar a cota free (250 req/dia).
        'Cache-Control': 'public, max-age=300, stale-while-revalidate=600'
    };

    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers, body: '' };
    }

    if (event.httpMethod !== 'GET') {
        return {
            statusCode: 405,
            headers,
            body: JSON.stringify({ error: 'Método Não Permitido. Utilize GET.' })
        };
    }

    const params = event.queryStringParameters || {};
    const path = params.path || '';

    if (!path || !path.startsWith('/')) {
        return {
            statusCode: 400,
            headers,
            body: JSON.stringify({ error: 'Parâmetro "path" obrigatório (ex.: /tournaments/1986).' })
        };
    }

    const permitido = ALLOWED_PREFIXES.some(p => path === p || path.startsWith(p + '/') || path.startsWith(p + '?'));
    if (!permitido) {
        return {
            statusCode: 403,
            headers,
            body: JSON.stringify({ error: 'Endpoint não permitido por este proxy.', path })
        };
    }

    const apiKey = process.env.ZAFRONIX_API_KEY || '';
    if (!apiKey) {
        console.error('ERRO: Variável de ambiente ZAFRONIX_API_KEY não foi encontrada.');
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({
                error: 'Chave da Zafronix não configurada no servidor.',
                details: 'Registre a variável de ambiente ZAFRONIX_API_KEY no painel do Netlify.'
            })
        };
    }

    // Repassa quaisquer query params extras (ex.: year, stage, limit), exceto o "path".
    const extras = new URLSearchParams();
    for (const [k, v] of Object.entries(params)) {
        if (k !== 'path' && v != null) extras.append(k, v);
    }
    const sep = path.includes('?') ? '&' : '?';
    const extrasStr = extras.toString();
    const apiUrl = `${API_BASE}${path}${extrasStr ? sep + extrasStr : ''}`;

    try {
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'X-API-Key': apiKey,
                'Accept': 'application/json'
            }
        });

        const text = await response.text();

        if (!response.ok) {
            console.error('ERRO na Zafronix API:', response.status, text);
            return {
                statusCode: response.status,
                headers,
                body: JSON.stringify({
                    error: `A Zafronix API retornou erro: ${response.status}`,
                    details: text
                })
            };
        }

        return { statusCode: 200, headers, body: text };
    } catch (err) {
        console.error('Falha de processamento no proxy Zafronix:', err);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({
                error: 'Falha interna no proxy serverless da Zafronix.',
                details: err.message
            })
        };
    }
};
