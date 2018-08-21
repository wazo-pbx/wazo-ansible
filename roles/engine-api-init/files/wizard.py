#!/usr/bin/python3

import argparse

from xivo_confd_client import Client as Confd


def init_uc_engine(entity_name, language, number_start, number_end, password):
    c = Confd('localhost', port=9486, https=True, verify_certificate=False)

    if c.wizard.get()['configured'] is not True:
        discover = c.wizard.discover()
    else:
        raise Exception("Wizard already configured...")

    wizard = {
      "admin_password": password,
      "license": True,
      "timezone": discover['timezone'],
      "language": language,
      "entity_name": entity_name,
      "network": {
        "hostname": discover['hostname'],
        "domain": discover['domain'],
        "interface": discover['interfaces'][0]['interface'],
        "ip_address": discover['interfaces'][0]['ip_address'],
        "netmask": discover['interfaces'][0]['netmask'],
        "gateway": discover['gateways'][0]['gateway'],
        "nameservers": discover['nameservers']
      },
      "context_incall": {
        "display_name": "Incalls",
        "did_length": 4
      },
      "context_internal": {
         "display_name": "Default",
         "number_start": number_start,
         "number_end": number_end
      },
      "context_outcall": {
         "display_name": "Outcalls"
      },
      "steps": {
         "manage_services": False,
         "manage_hosts_file": False,
         "manage_resolv_file": False,
         "commonconf": False,
         "phonebook": False,
      }
    }

    return c.wizard.create(wizard)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--entity-name', action='store')
    parser.add_argument('--language', action='store')
    parser.add_argument('--number-start', action='store')
    parser.add_argument('--number-end', action='store')
    parser.add_argument('--password', action='store')
    parser.add_argument('--no-fail', action='store_true')
    return parser.parse_args()


def main():
    args = _parse_args()
    try:
        init_uc_engine(args.entity_name,
                       args.language,
                       args.number_start,
                       args.number_end,
                       args.password)
    except Exception:
        if not args.no_fail:
            raise


if __name__ == '__main__':
    main()
