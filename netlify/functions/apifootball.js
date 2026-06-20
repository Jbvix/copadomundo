/**
 * Nome do Autor: Jossian Brito
 * Data: 20/06/2026
 * Versão: 1.0.0
 *
 * Proxy serverless para a API-Football (https://v3.football.api-sports.io).
 * - Mantém a APIFOOTBALL_API_KEY exclusivamente no servidor (nunca exposta ao cliente).
 * - Fonte primária dos jogos da Copa 2026 (livescore a cada ~15s, eventos, escalações).
 * - Allowlist de endpoints para evitar SSRF/uso indevido do proxy.
 * - Cache no CDN do Netlify para preservar a cota diária (plano free: 100 req/dia).
 * - Usa o fetch nativo do Node 18+ (sem dependências externas).
 */

const API_BASE = 'https://v3.football.api-sports.io';

const ALLOWED_PREFIXES = [
    '/fixtures',
    '/standings',
    '/teams',
    '/players',
    '/leagues'
];

exports.handler = async function (event) {
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Content-Type': 'application/json',
        // Cache curto no CDN: ao vivo continua fresco, mas evita estourar a cota.
        'Cache-Control': 'public, max-age=30, stale-while-revalidate=120'
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
            body: JSON.stringify({ error: 'Parâmetro "path" obrigatório (ex.: /fixtures).' })
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

    // Aceita diferentes nomes de variável para não depender de uma grafia exata.
    const env = process.env;
    const apiKey = env.APIFOOTBALL_API_KEY
        || env.x_apisports_key
        || env.X_APISPORTS_KEY
        || env.APISPORTS_KEY
        || env.API_FOOTBALL_KEY
        || env.APIFOOTBALL_KEY
        || '';
    if (!apiKey) {
        console.error('ERRO: Nenhuma variável de ambiente com a chave da API-Football foi encontrada.');
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({
                error: 'Chave da API-Football não configurada no servidor.',
                details: 'Registre a chave no painel do Netlify (ex.: APIFOOTBALL_API_KEY ou x_apisports_key).'
            })
        };
    }

    // Repassa os demais query params (ex.: league, season, fixture, live), exceto "path".
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
                'x-apisports-key': apiKey,
                'Accept': 'application/json'
            }
        });

        const text = await response.text();

        if (!response.ok) {
            console.error('ERRO na API-Football:', response.status, text);
            return {
                statusCode: response.status,
                headers,
                body: JSON.stringify({
                    error: `A API-Football retornou erro: ${response.status}`,
                    details: text
                })
            };
        }

        return { statusCode: 200, headers, body: text };
    } catch (err) {
        console.error('Falha de processamento no proxy API-Football:', err);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({
                error: 'Falha interna no proxy serverless da API-Football.',
                details: err.message
            })
        };
    }
};
