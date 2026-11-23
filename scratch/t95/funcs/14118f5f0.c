char __fastcall sub_14118F5F0(__int64 a1, int a2, __int64 **a3)
{
  __int64 v5; // rbx
  __int64 v6; // rbx
  __int64 v7; // rbx
  __int64 v8; // rdx
  volatile signed __int32 **v9; // rsi
  __int64 v10; // rsi
  volatile signed __int32 *v12; // rax
  volatile signed __int32 *v13; // rcx
  volatile signed __int32 *v14; // rdi
  volatile signed __int32 *v15; // rdi
  __int64 v16; // rcx
  _QWORD v17[5]; // [rsp+20h] [rbp-28h] BYREF

  if ( a2 <= 1095250530 )
  {
    if ( a2 > 1093886310 )
    {
      switch ( a2 )
      {
        case 1095250275:
          v6 = qword_141B5FDD0;
          sub_140FE7960(v17, a3, 1315856756);
          *(_QWORD *)(a1 + 40) = sub_14002F670(v6, v17);
          return 1;
        case 1095250276:
        case 1095250277:
        case 1095250278:
        case 1095250279:
        case 1095250280:
        case 1095250282:
        case 1095250283:
        case 1095250284:
        case 1095250285:
        case 1095250287:
        case 1095250289:
        case 1095250290:
        case 1095250291:
          return sub_140FE2700((_DWORD *)a1, a2, a3);
        case 1095250281:
          if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
            *(_WORD *)(a1 + 142) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 80))(*a3, a3);
          else
            *(_WORD *)(a1 + 142) = 0;
          return 1;
        case 1095250286:
          (*(void (__fastcall **)(__int64 *, _QWORD *, __int64 **))(**a3 + 128))(*a3, v17, a3);
          v9 = (volatile signed __int32 **)(a1 + 80);
LABEL_55:
          if ( v9 != v17 )
          {
            v8 = v17[0];
            v12 = *v9;
            v13 = *v9 - 1;
            if ( *v9 == nullptr )
              v13 = nullptr;
            v14 = (volatile signed __int32 *)(v17[0] - 4LL);
            if ( v17[0] != 0 )
            {
              if ( v12 != nullptr && _InterlockedDecrement(v13) == 0 )
                sub_1412EC9A0(v13, v8);
              *v9 = nullptr;
              _InterlockedIncrement(v14);
              v15 = v14 + 1;
            }
            else
            {
              if ( v12 != nullptr && _InterlockedDecrement(v13) == 0 )
                sub_1412EC9A0(v13, v8);
              v15 = nullptr;
            }
            *v9 = v15;
          }
          v16 = v17[0];
          if ( v17[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v17[0] - 4LL)) == 0 )
            sub_1412EC9A0(v16 - 4, v8);
          return 1;
        case 1095250288:
          v10 = a1 + 32;
LABEL_64:
          sub_140FE8040(v10, a3);
          return 1;
        case 1095250292:
          sub_140FE7960(v17, a3, 1416914273);
          *(_QWORD *)(a1 + 104) = v17[0];
          return 1;
        default:
          if ( a2 == 1093886311 )
          {
            if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
              *(_BYTE *)(a1 + 154) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
            else
              *(_BYTE *)(a1 + 154) = 0;
          }
          else
          {
            if ( a2 != 1093888306 )
              return sub_140FE2700((_DWORD *)a1, a2, a3);
            if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
              *(_WORD *)(a1 + 152) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 80))(*a3, a3);
            else
              *(_WORD *)(a1 + 152) = 0;
          }
          break;
      }
      return 1;
    }
    if ( a2 > 1093820774 )
    {
      if ( a2 == 1093820775 )
      {
        if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
          *(_BYTE *)(a1 + 156) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
        else
          *(_BYTE *)(a1 + 156) = 0;
        return 1;
      }
      if ( a2 == 1093822770 )
      {
        if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
          *(_WORD *)(a1 + 148) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 80))(*a3, a3);
        else
          *(_WORD *)(a1 + 148) = 0;
        return 1;
      }
    }
    else
    {
      if ( a2 == 1093755239 )
      {
        if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
          *(_BYTE *)(a1 + 155) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
        else
          *(_BYTE *)(a1 + 155) = 0;
        return 1;
      }
      if ( a2 == 1093757234 )
      {
        if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
          *(_WORD *)(a1 + 144) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 80))(*a3, a3);
        else
          *(_WORD *)(a1 + 144) = 0;
        return 1;
      }
    }
    return sub_140FE2700((_DWORD *)a1, a2, a3);
  }
  if ( a2 <= 1095265891 )
  {
    switch ( a2 )
    {
      case 1095250531:
        v7 = qword_141B5FDD0;
        sub_140FE7960(v17, a3, 1315856756);
        *(_QWORD *)(a1 + 56) = sub_14002F670(v7, v17);
        return 1;
      case 1095250532:
      case 1095250533:
      case 1095250534:
      case 1095250535:
      case 1095250536:
      case 1095250538:
      case 1095250539:
      case 1095250540:
      case 1095250541:
      case 1095250543:
      case 1095250545:
      case 1095250546:
      case 1095250547:
        return sub_140FE2700((_DWORD *)a1, a2, a3);
      case 1095250537:
        if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
          *(_WORD *)(a1 + 146) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 80))(*a3, a3);
        else
          *(_WORD *)(a1 + 146) = 0;
        return 1;
      case 1095250542:
        (*(void (__fastcall **)(__int64 *, _QWORD *, __int64 **))(**a3 + 128))(*a3, v17, a3);
        v9 = (volatile signed __int32 **)(a1 + 88);
        goto LABEL_55;
      case 1095250544:
        v10 = a1 + 48;
        goto LABEL_64;
      case 1095250548:
        sub_140FE7960(v17, a3, 1416914273);
        *(_QWORD *)(a1 + 112) = v17[0];
        return 1;
      default:
        switch ( a2 )
        {
          case 1095250787:
            v5 = qword_141B5FDD0;
            sub_140FE7960(v17, a3, 1315856756);
            *(_QWORD *)(a1 + 64) = sub_14002F670(v5, v17);
            return 1;
          case 1095250793:
            if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
              *(_WORD *)(a1 + 150) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 80))(*a3, a3);
            else
              *(_WORD *)(a1 + 150) = 0;
            return 1;
          case 1095250798:
            (*(void (__fastcall **)(__int64 *, _QWORD *, __int64 **))(**a3 + 128))(*a3, v17, a3);
            v9 = (volatile signed __int32 **)(a1 + 96);
            goto LABEL_55;
          case 1095250800:
            v10 = a1 + 72;
            goto LABEL_64;
          case 1095250804:
            sub_140FE7960(v17, a3, 1416914273);
            *(_QWORD *)(a1 + 120) = v17[0];
            return 1;
          default:
            return sub_140FE2700((_DWORD *)a1, a2, a3);
        }
    }
  }
  if ( a2 > 1095266354 )
  {
    switch ( a2 )
    {
      case 1095266355:
        *(_DWORD *)(a1 + 136) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 80))(*a3, a3);
        return 1;
      case 1097363060:
        *(_BYTE *)(a1 + 158) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3);
        return 1;
      case 1095268709:
        *(_WORD *)(a1 + 140) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
        return 1;
      default:
        break;
    }
    return sub_140FE2700((_DWORD *)a1, a2, a3);
  }
  if ( a2 == 1095265892 )
  {
    *(_BYTE *)(a1 + 157) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3);
    return 1;
  }
  if ( a2 == 1095266353 )
  {
    *(_DWORD *)(a1 + 128) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 80))(*a3, a3);
    return 1;
  }
  if ( a2 != 1095266354 )
    return sub_140FE2700((_DWORD *)a1, a2, a3);
  *(_DWORD *)(a1 + 132) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 80))(*a3, a3);
  return 1;
}
