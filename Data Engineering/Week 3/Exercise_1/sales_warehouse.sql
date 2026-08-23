--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: dim_customer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dim_customer (
    customer_id integer NOT NULL,
    customer_name character varying(100),
    city character varying(100),
    country character varying(100)
);


ALTER TABLE public.dim_customer OWNER TO postgres;

--
-- Name: dim_date; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dim_date (
    date_id integer NOT NULL,
    full_date date,
    month integer,
    year integer
);


ALTER TABLE public.dim_date OWNER TO postgres;

--
-- Name: dim_product; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dim_product (
    product_id integer NOT NULL,
    product_name character varying(100),
    category character varying(100),
    price numeric(10,2)
);


ALTER TABLE public.dim_product OWNER TO postgres;

--
-- Name: dim_store; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dim_store (
    store_id integer NOT NULL,
    store_name character varying(100),
    city character varying(100)
);


ALTER TABLE public.dim_store OWNER TO postgres;

--
-- Name: fact_sales; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fact_sales (
    sale_id integer NOT NULL,
    customer_id integer,
    product_id integer,
    date_id integer,
    store_id integer,
    quantity integer,
    sales_amount numeric(10,2)
);


ALTER TABLE public.fact_sales OWNER TO postgres;

--
-- Data for Name: dim_customer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dim_customer (customer_id, customer_name, city, country) FROM stdin;
1	Rahul	Ahmedabad	India
2	Priya	Mumbai	India
3	Amit	Delhi	India
\.


--
-- Data for Name: dim_date; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dim_date (date_id, full_date, month, year) FROM stdin;
1	2026-01-10	1	2026
2	2026-01-15	1	2026
3	2026-02-05	2	2026
\.


--
-- Data for Name: dim_product; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dim_product (product_id, product_name, category, price) FROM stdin;
1	Laptop	Electronics	60000.00
2	Mouse	Electronics	1000.00
3	Chair	Furniture	5000.00
\.


--
-- Data for Name: dim_store; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dim_store (store_id, store_name, city) FROM stdin;
1	Ahmedabad Store	Ahmedabad
2	Mumbai Store	Mumbai
\.


--
-- Data for Name: fact_sales; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fact_sales (sale_id, customer_id, product_id, date_id, store_id, quantity, sales_amount) FROM stdin;
1	1	1	1	1	1	60000.00
2	2	2	1	2	2	2000.00
3	3	3	2	1	1	5000.00
4	1	2	3	1	3	3000.00
\.


--
-- Name: dim_customer dim_customer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dim_customer
    ADD CONSTRAINT dim_customer_pkey PRIMARY KEY (customer_id);


--
-- Name: dim_date dim_date_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dim_date
    ADD CONSTRAINT dim_date_pkey PRIMARY KEY (date_id);


--
-- Name: dim_product dim_product_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dim_product
    ADD CONSTRAINT dim_product_pkey PRIMARY KEY (product_id);


--
-- Name: dim_store dim_store_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dim_store
    ADD CONSTRAINT dim_store_pkey PRIMARY KEY (store_id);


--
-- Name: fact_sales fact_sales_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fact_sales
    ADD CONSTRAINT fact_sales_pkey PRIMARY KEY (sale_id);


--
-- Name: fact_sales fact_sales_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fact_sales
    ADD CONSTRAINT fact_sales_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.dim_customer(customer_id);


--
-- Name: fact_sales fact_sales_date_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fact_sales
    ADD CONSTRAINT fact_sales_date_id_fkey FOREIGN KEY (date_id) REFERENCES public.dim_date(date_id);


--
-- Name: fact_sales fact_sales_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fact_sales
    ADD CONSTRAINT fact_sales_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.dim_product(product_id);


--
-- Name: fact_sales fact_sales_store_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fact_sales
    ADD CONSTRAINT fact_sales_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.dim_store(store_id);


--
-- PostgreSQL database dump complete
--

