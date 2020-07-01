import urllib.parse
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug


class JSONTypes():

    @staticmethod
    def productJSON(name, item_id, code, price, attribute_line_ids, variants, configurable_children,
                    size_attribute_name, color_attribute_name, host_odoo):

        # Configurable options
        configurable_options_array = []
        for variant in variants:
            configurable_options_array.append(
                JSONTypes.configurable_option_JSON(
                    variant,
                    item_id,
                    size_attribute_name,
                    color_attribute_name
                )
            )

        # Configurable children
        configurable_children_array = []
        for configurable in configurable_children:
            configurable_children_array.append(
                JSONTypes.configurable_children_JSON(
                    name,
                    configurable,
                    item_id,
                    size_attribute_name,
                    color_attribute_name,
                    host_odoo
                )
            )

        # First variant id
        first_variant_id = configurable_children[0].get("id")
        get_id_product_template = request.env['product.template'].sudo().search([('id', '=', item_id)])
        print("LINE 38")
        print(get_id_product_template)
        status_product = '2' if str(get_id_product_template.active) == 't' else '1' if float(
            get_id_product_template.virtual_available) <= 0 else '3'
        media_gallery = []
        get_id_img_product_template = request.env['product.image'].sudo().search([('product_tmpl_id', '=', item_id)])
        for val_get_id_img_product_template in get_id_img_product_template:
            media_gallery.append({
                "image": "/web/image/product.image/" + str(val_get_id_img_product_template) + "/image",
                "pos": str(val_get_id_img_product_template.sequence),
                "typ": "image",
                "lab": 'null',
                "vid": 'null',
            })
        # https://github.com/DivanteLtd/storefront-integration-sdk/blob/tutorial/Format-product.md
        source = {
            # id,name,img,sku,url_key,url_path,type_id,price,special_price,price_incl_tax,special_price_incl_tax,special_to_date,special_from_date,status,visibility,size,color,[size_option],[color_option],[category_ids],[category],[media_gallery],[configurable_option],[stock],[configuable_children]
            "id": 1,
            "name": name,
            "image": host_odoo + "/web/image/product.product/" + str(first_variant_id) + "/image",
            "sku": str(item_id),
            "url_key": JSONTypes.url_key(name),
            "url_path": 'null',
            "type_id": "configurable",
            "special_price": price,
            "price_incl_tax": 'null',
            "special_price_incl_tax": 'null',
            "special_to_date": 'null',
            "special_from_date": 'null',
            "status": status_product,
            "visibility": '4' if int(status_product) != 2 else '1',
            "size": 'null',
            "color": 'null',
            "size_options": [],
            "color_options": [],
            "category_ids": [get_id_product_template.categ_id.id],
            "category": [{
                "category_id": str(get_id_product_template.categ_id.id),
                "name": str(get_id_product_template.categ_id.name),
                "slug": str(get_id_product_template.categ_id.name),
                "path": 'null',
                # "path": str(request.httprequest.path.split('/')),
            }],
            "media_gallery": media_gallery,
            "configurable_options": configurable_options_array,
            "stock": [{"is_in_stock": '1', "qty": str(get_id_product_template.virtual_available)}],
            # "attribute_line_ids": attribute_line_ids,
            # "variants": variants,
            "configurable_children": configurable_children_array,
            # "pattern": "197",
            # "description": "La nueva temporada llega con un estilo que te renovará de pies a cabeza como nunca antes. Los nuevos colores de la temporada 2019 llegan para quedarse en esta nueva colección con la marca como protagonista de tu nuevo estilo.",
            # "eco_collection": "1",
            # # START OF CONFIGURABLE OPTIONS
            # "configurable_options_original": variants,
            # "configurable_options": configurable_options_array,
            # # END OF CONFIGURABLE OPTIONS
            # "tsk": 1551705236617,
            # "custom_attributes": None,
            # "size_options": [],
            # "regular_price": 29,
            # "erin_recommends": "0",
            # "final_price": price,
            # "price": 29,
            # "color_options": [],
            # "links": {},
            # "id": item_id,
            # "category_ids": [
            #     "25",
            #     "33",
            #     "8",
            #     "36",
            #     "2"
            # ],
            # "sku": str(item_id),
            # "stock": {
            #     "min_sale_qty": 1,
            #     "item_id": item_id,
            #     "min_qty": 0,
            #     "stock_status_changed_auto": 0,
            #     "is_in_stock": True,
            #     "max_sale_qty": 10000,
            #     "show_default_notification_message": False,
            #     "backorders": 0,
            #     "product_id": item_id,
            #     "qty": 0,
            #     "is_decimal_divided": False,
            #     "is_qty_decimal": False,
            #     "low_stock_date": None,
            #     "use_config_qty_increments": True
            # },
            # "slug": code,
            # "url_path": code,
            # "image": host_odoo + "/web/image/product.product/" + str(first_variant_id) + "/image",
            # "new": "1",
            # "thumbnail": host_odoo + "/web/image/product.product/" + str(first_variant_id) + "/image",
            # "visibility": 4,
            # "type_id": "configurable",
            # "tax_class_id": "2",
            # "media_gallery": [],
            # "climate": "205,209",
            # "style_general": "136",
            # "url_key": JSONTypes.url_key(name),
            # "performance_fabric": "0",
            # "sale": "0",
            # "max_price": price,
            # "minimal_regular_price": price,
            # "material": "153,154",
            # "special_price": 0,
            # "minimal_price": price,
            # "name": name,
            # # START OF CONFIGURABLE CHILDREN
            # "configurable_children_original": configurable_children,
            # "configurable_children": configurable_children_array,
            # # END OF CONFIGURABLE CHILDREN
            # "max_regular_price": price,
            # "category": [],
            # "status": 1,
            # "priceTax": 6.67,
            # "priceInclTax": price,
            # "specialPriceTax": None,
            # "specialPriceInclTax": None
        }
        return source
        # return {
        #     "_source": source,
        #     "_score": 1
        # }

    @staticmethod
    def configurable_option_JSON(variant, item_id, size_attribute_name, color_attribute_name):

        attribute_id = variant.get("attribute_id")[0]
        attribute_name = variant.get("attribute_id")[1]

        attribute_label_json = 'null'
        attribute_code_json = 'null'

        if attribute_name == size_attribute_name:
            attribute_label_json = "Size"
            attribute_code_json = "size"
        elif attribute_name == color_attribute_name:
            attribute_label_json = "Color"
            attribute_code_json = "color"

        values_array = []
        attributes = variant.get("attributes")
        for attribute in attributes:

            if attribute_name == size_attribute_name:
                values_array.append({
                    "value_index": attribute[0].get("id"),
                    "label": str(attribute[0].get("name")),
                })
            elif attribute_name == color_attribute_name:
                values_array.append({
                    "value_index": attribute[0].get("id"),
                    "label": "#" + str(attribute[0].get("html_color")),
                })

        result = {
            "id": attribute_id,
            "attribute_id": attribute_id,
            "label": attribute_label_json,
            "position": 0,
            "values": values_array,
            "product_id": item_id,
            "attribute_code": attribute_code_json
        }
        return result

    @staticmethod
    def url_key(name):
        return urllib.parse.quote_plus(name).lower().replace("+", "-")

    @staticmethod
    def configurable_children_JSON(name, configurable, item_id, size_attribute_name, color_attribute_name, host_odoo):

        # Get size and color
        size_id = 'null'
        color_id = 'null'
        attributes = configurable.get("attributes")
        for attribute in attributes:
            if attribute:
                attribute_name = attribute[0].get("attribute_id")[1]

                if attribute_name == size_attribute_name:
                    size_id = attribute[0].get("id")
                elif attribute_name == color_attribute_name:
                    color_id = attribute[0].get("id")

        size_id_string = str(size_id)
        color_id_string = str(color_id)

        result = {
            "type_id": 'null',
            "sku": str(configurable.get("id")),
            "special_price": 0,
            "special_to_date": 'null',
            "special_from_date": 'null',
            "name": name,
            "price": 'null',
            "priceInclTax": configurable.get("list_price"),
            "specialPriceInclTax": '',
            "id": configurable.get("id"),
            "image": host_odoo + "/web/image/product.product/" + str(configurable.get("id")) + "/image",
            "url_key": JSONTypes.url_key(name),
            "url_path": 'null',
            "status": 1,
            "size": size_id_string,
            "color": color_id_string,
            # "thumbnail": host_odoo + "/web/image/product.product/" + str(configurable.get("id")) + "/image",
            # "small_image": host_odoo + "/web/image/product.product/" + str(configurable.get("id")) + "/image",
            # "tax_class_id": "2",
            # "has_options": "0",
            # "regular_price": configurable.get("list_price"),
            # "required_options": "0",
            # "max_price": configurable.get("list_price"),
            # "minimal_regular_price": configurable.get("list_price"),
            # "final_price": configurable.get("list_price"),
            # "minimal_price": configurable.get("list_price"),
            # "name": size_id_string + "-" + color_id_string,
            # "category_ids": [],
            # "max_regular_price": configurable.get("list_price"),
            # "priceTax": 6.67,
            # "specialPriceTax": None,
        }
        return result

    @staticmethod
    def attributeJSON(attribute_id, attribute_code, default_frontend_label):
        return {
            "is_wysiwyg_enabled": False,
            "is_html_allowed_on_front": True,
            "used_for_sort_by": False,
            "is_filterable": True,
            "is_filterable_in_search": False,
            "is_used_in_grid": False,
            "is_visible_in_grid": False,
            "is_filterable_in_grid": False,
            "position": 0,
            "apply_to": [],
            "is_searchable": "0",
            "is_visible_in_advanced_search": "0",
            "is_comparable": "0",
            "is_used_for_promo_rules": "1",
            "is_visible_on_front": "0",
            "used_in_product_listing": "1",
            "is_visible": True,
            "scope": "global",
            "attribute_id": attribute_id,
            "attribute_code": attribute_code,
            "frontend_input": "select",
            "entity_type_id": "4",
            "is_required": False,
            "options": [],
            "is_user_defined": True,
            "default_frontend_label": default_frontend_label,
            "frontend_labels": None,
            "backend_type": "int",
            "is_unique": "0",
            "validation_rules": [],
            "id": 142,
            "tsk": 1512134647691,
            "default_value": "91",
            "source_model": "Magento\\Eav\\Model\\Entity\\Attribute\\Source\\Table",
            "sgn": "vHkjS2mGumtgjjzlDrGJnF6i8EeUU2twc2zkZe69ABc"
        }

    @staticmethod
    def category_json(name, id, parent_id, childs, parent_path, sequence, level, category_offset):
        children_data = []
        for child in childs:
            children_data.append({
                "id": child
            })
        children_count = len(children_data)

        # if children_count == 0:
        #     result = {
        #         "_index":"vue_storefront_catalog_1552559102",
        #         "_type":"category",
        #         "_id": id,
        #         "_score": None,
        #         "_source":{
        #             "path":"1/2/20",
        #             "is_active": True,
        #             "level": level,
        #             "product_count":1,
        #             "children_count": str(children_count),
        #             "parent_id": parent_id,
        #             "name": name,
        #             "id": id + category_offset,
        #             "url_path": "categories/category-" + str(id + category_offset),
        #             "url_key": str(id + category_offset),
        #         },
        #         "sort":[
        #             2
        #         ]
        #     }
        # else:
        #     result = {
        #         "_index": "vue_storefront_catalog_1552559102",
        #         "_type": "category",
        #         "_id": id,
        #         "_score": None,
        #         "_source": {
        #             "path": "1/2/20",
        #             "is_active": True,
        #             "level": level,
        #             "product_count": 1,
        #             "children_count": str(children_count),
        #             "parent_id": parent_id,
        #             "name": name,
        #             "id": id + category_offset,
        #             "url_path": "categories/category-" + str(id + category_offset),
        #             "url_key": str(id + category_offset),
        #             "children_data": children_data
        #         },
        #         "sort": [
        #             2
        #         ]
        #     }
        get_id_product_template = request.env['product.template'].sudo().search([('public_categ_ids', '=', id)])
        print("LINE 338")
        print(get_id_product_template)
        result = {
            "id": id,
            "name": name,
            "url_key": str(id + category_offset),
            "path": str(parent_path),
            "url_path": "categories/category-" + str(id + category_offset),
            "is_active": True,
            "position": sequence,
            "level": level,
            "product_count": len(get_id_product_template),
            "children_data": children_data,
        }

        return result

    @staticmethod
    def categories_to_response(categories, level, parent_id, category_offset):
        categories_array = []
        for category in categories:
            categories_array.append(JSONTypes.category_json(
                category["name"],
                category["id"],
                category["parent_id"],
                category["child_id"],
                category["parent_path"],
                category["sequence"],
                len(str(category["parent_path"]).split('/')),
                category_offset
            ))

        # response = {
        #     "took": 1,
        #     "timed_out": False,
        #     "_shards": {
        #         "total": 5,
        #         "successful": 5,
        #         "skipped": 0,
        #         "failed": 0
        #     },
        #     "hits": {
        #         "total": 6,
        #         "max_score": None,
        #         "hits": categories_array
        #     }
        # }
        response = categories_array
        return response

    @staticmethod
    def attributeJSON(
            is_html_allowed_on_front,
            used_for_sort_by,
            is_used_in_grid,
            is_filterable_in_grid,
            apply_to,
            is_searchable,
            is_visible_in_advanced_search,
            is_used_for_promo_rules,
            used_in_product_listing,
            attribute_id,
            attribute_code,
            frontend_input,
            is_required,
            options,
            is_user_defined,
            default_frontend_label,
            backend_type,
            backend_model,
            source_model,
            default_value,
            id
    ):
        response = {
            "is_wysiwyg_enabled": False,
            "is_html_allowed_on_front": is_html_allowed_on_front,
            "used_for_sort_by": used_for_sort_by,
            "is_filterable": True,
            "is_filterable_in_search": False,
            "is_used_in_grid": is_used_in_grid,
            "is_visible_in_grid": False,
            "is_filterable_in_grid": is_filterable_in_grid,
            "position": 0,
            "apply_to": apply_to,
            "is_searchable": is_searchable,
            "is_visible_in_advanced_search": is_visible_in_advanced_search,
            "is_comparable": "0",
            "is_used_for_promo_rules": is_used_for_promo_rules,
            "is_visible_on_front": "0",
            "used_in_product_listing": used_in_product_listing,
            "is_visible": True,
            "scope": "global",
            "attribute_id": attribute_id,
            "attribute_code": attribute_code,
            "frontend_input": frontend_input,
            "entity_type_id": "4",
            "is_required": is_required,
            "options": options,
            "is_user_defined": is_user_defined,
            "default_frontend_label": default_frontend_label,
            "frontend_labels": None,
            "backend_type": backend_type,
            "backend_model": backend_model,
            "source_model": source_model,
            "default_value": default_value,
            "is_unique": "0",
            "validation_rules": [

            ],
            "id": id,
            "tsk": 1551705231251
        }
        return response

    @staticmethod
    def order_json(
            order_id,
            confirmation_date,
            amount_total,
            amount_tax,
            amount_untaxed,
            shipping_amount,
            discount_amount,
            items_array,
            name,
            lastname,
            city,
            postcode,
            street,
    ):
        result = {
            "applied_rule_ids": "1,5",
            "base_currency_code": "USD",
            "base_discount_amount": (-1) * discount_amount,
            "base_grand_total": amount_total,
            "base_discount_tax_compensation_amount": 0,
            "base_shipping_amount": shipping_amount,
            "base_shipping_discount_amount": 0,
            "base_shipping_incl_tax": shipping_amount,
            "base_shipping_tax_amount": 0,
            "base_subtotal": amount_untaxed,
            "base_subtotal_incl_tax": amount_total,
            "base_tax_amount": amount_tax,
            "base_total_due": amount_total,
            "base_to_global_rate": 1,
            "base_to_order_rate": 1,
            "billing_address_id": 204,
            "created_at": confirmation_date,
            "customer_email": "pkarwatka28@example.com",
            "customer_group_id": 0,
            "customer_is_guest": 1,
            "customer_note_notify": 1,
            "discount_amount": (-1) * discount_amount,
            "email_sent": 1,
            "entity_id": order_id,
            "global_currency_code": "USD",
            "grand_total": amount_total,
            "discount_tax_compensation_amount": 0,
            "increment_id": str(order_id),
            "is_virtual": 0,
            "order_currency_code": "USD",
            "protect_code": "3984835d33abd2423b8a47efd0f74579",
            "quote_id": 1112,
            "shipping_amount": shipping_amount,
            "shipping_description": "Flat Rate - Fixed",
            "shipping_discount_amount": 0,
            "shipping_discount_tax_compensation_amount": 0,
            "shipping_incl_tax": shipping_amount,
            "shipping_tax_amount": 0,
            "state": "new",
            "status": "pending",
            "store_currency_code": "USD",
            "store_id": 1,
            "store_name": "Main Website\nMain Website Store\n",
            "store_to_base_rate": 0,
            "store_to_order_rate": 0,
            "subtotal": amount_untaxed,
            "subtotal_incl_tax": amount_total,
            "tax_amount": amount_tax,
            "total_due": amount_total,
            "total_item_count": 1,
            "total_qty_ordered": 1,
            "updated_at": confirmation_date,
            "weight": 1,
            "items": items_array,
            "billing_address": {
                "address_type": "billing",
                "city": city,
                "company": "Divante",
                "country_id": "PL",
                "email": "pkarwatka28@example.com",
                "entity_id": 204,
                "firstname": name,
                "lastname": lastname,
                "parent_id": order_id,
                "postcode": postcode,
                "street": [
                    street,
                    ""
                ],
                "telephone": None,
                "vat_id": "PL8951930748"
            },
            "payment": {
                "account_status": None,
                "additional_information": [
                    "Cash On Delivery",
                    ""
                ],
                "amount_ordered": amount_total,
                "base_amount_ordered": amount_total,
                "base_shipping_amount": shipping_amount,
                "cc_last4": None,
                "entity_id": order_id,
                "method": "cashondelivery",
                "parent_id": order_id,
                "shipping_amount": 5
            },
            "status_histories": [],
            "extension_attributes": {
                "shipping_assignments": [
                    {
                        "shipping": {
                            "address": {
                                "address_type": "shipping",
                                "city": city,
                                "company": "NA",
                                "country_id": "PL",
                                "email": "pkarwatka28@example.com",
                                "entity_id": 203,
                                "firstname": name,
                                "lastname": lastname,
                                "parent_id": order_id,
                                "postcode": postcode,
                                "street": [
                                    street,
                                    ""
                                ],
                                "telephone": None
                            },
                            "method": "flatrate_flatrate",
                            "total": {
                                "base_shipping_amount": shipping_amount,
                                "base_shipping_discount_amount": 0,
                                "base_shipping_incl_tax": shipping_amount,
                                "base_shipping_tax_amount": 0,
                                "shipping_amount": shipping_amount,
                                "shipping_discount_amount": 0,
                                "shipping_discount_tax_compensation_amount": 0,
                                "shipping_incl_tax": shipping_amount,
                                "shipping_tax_amount": 0
                            }
                        },
                        "items": items_array
                    }
                ]
            }
        }
        return result

    @staticmethod
    def order_item_json(
            order_id,
            confirmation_date,
            item_name,
            sku,
            price_unit_with_tax,
            quantity,
            row_total_with_tax,
            discount_amount,
    ):
        result = {
            "amount_refunded": 0,
            "applied_rule_ids": "1,5",
            "base_amount_refunded": 0,
            "base_discount_amount": discount_amount,
            "base_discount_invoiced": 0,
            "base_discount_tax_compensation_amount": 0,
            "base_original_price": 22,
            "base_price": 22,
            "base_price_incl_tax": price_unit_with_tax,
            "base_row_invoiced": 0,
            "base_row_total": 22,
            "base_row_total_incl_tax": row_total_with_tax,
            "base_tax_amount": 4.3,
            "base_tax_invoiced": 0,
            "created_at": confirmation_date,
            "discount_amount": discount_amount,
            "discount_invoiced": 0,
            "discount_percent": 15,
            "free_shipping": 0,
            "discount_tax_compensation_amount": 0,
            "is_qty_decimal": 0,
            "is_virtual": 0,
            "item_id": 224,
            "name": item_name,
            "no_discount": 0,
            "order_id": order_id,
            "original_price": 22,
            "price": 22,
            "price_incl_tax": price_unit_with_tax,
            "product_id": 1546,
            "product_type": "simple",
            "qty_canceled": 0,
            "qty_invoiced": 0,
            "qty_ordered": 1,
            "qty_refunded": 0,
            "qty_shipped": 0,
            "quote_item_id": 675,
            "row_invoiced": 0,
            "row_total": 22,
            "row_total_incl_tax": row_total_with_tax,
            "row_weight": 1,
            "sku": str(sku),
            "store_id": 1,
            "tax_amount": 4.3,
            "tax_invoiced": 0,
            "tax_percent": 23,
            "updated_at": confirmation_date,
            "weight": 1
        }
        return result
