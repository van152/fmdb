char __fastcall sub_1415826F0(__int64 a1, int a2, __int64 **a3)
{
  __int64 v5; // rdx
  volatile signed __int32 **v6; // rsi
  char v7; // al
  char v8; // cl
  volatile signed __int32 *v9; // rax
  volatile signed __int32 *v10; // rcx
  volatile signed __int32 *v11; // rdi
  volatile signed __int32 *v12; // rdi
  char v13; // al
  char v14; // cl
  char v15; // al
  char v16; // cl
  char v17; // al
  char v18; // cl
  char v19; // al
  char v20; // cl
  __int64 v22; // rcx
  _QWORD v23[4]; // [rsp+28h] [rbp-20h] BYREF

  if ( a2 <= 1231386723 )
  {
    if ( a2 <= 1231188071 )
    {
      if ( a2 <= 1231186285 )
      {
        if ( a2 == 1145392197 )
        {
          *(_WORD *)(a1 + 76) = -258;
          return 1;
        }
        if ( a2 == 1231120242 )
        {
          *(_BYTE *)(a1 + 81) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
          return 1;
        }
      }
      else
      {
        switch ( a2 )
        {
          case 1231186286:
            v17 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3);
            v18 = *(_BYTE *)(a1 + 87);
            if ( v17 != 0 )
              *(_BYTE *)(a1 + 87) = v18 | 4;
            else
              *(_BYTE *)(a1 + 87) = v18 & 0xFB;
            return 1;
          case 1231186291:
            v19 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3);
            v20 = *(_BYTE *)(a1 + 87);
            if ( v19 != 0 )
              *(_BYTE *)(a1 + 87) = v20 | 8;
            else
              *(_BYTE *)(a1 + 87) = v20 & 0xF7;
            return 1;
          case 1231188071:
            v7 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3);
            v8 = *(_BYTE *)(a1 + 87);
            if ( v7 != 0 )
              *(_BYTE *)(a1 + 87) = v8 | 0x10;
            else
              *(_BYTE *)(a1 + 87) = v8 & 0xEF;
            return 1;
          default:
            break;
        }
      }
    }
    else if ( a2 > 1231250543 )
    {
      switch ( a2 )
      {
        case 1231250544:
          if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
            *(_BYTE *)(a1 + 86) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
          else
            *(_BYTE *)(a1 + 86) = -1;
          return 1;
        case 1231252851:
          *(_BYTE *)(a1 + 82) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
          return 1;
        case 1231253358:
          *(_BYTE *)(a1 + 83) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3);
          return 1;
        default:
          break;
      }
    }
    else
    {
      switch ( a2 )
      {
        case 1231188072:
          v13 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3);
          v14 = *(_BYTE *)(a1 + 87);
          if ( v13 != 0 )
            *(_BYTE *)(a1 + 87) = v14 | 1;
          else
            *(_BYTE *)(a1 + 87) = v14 & 0xFE;
          return 1;
        case 1231188848:
          v15 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3);
          v16 = *(_BYTE *)(a1 + 87);
          if ( v15 != 0 )
            *(_BYTE *)(a1 + 87) = v16 | 2;
          else
            *(_BYTE *)(a1 + 87) = v16 & 0xFD;
          return 1;
        case 1231249781:
          *(_WORD *)(a1 + 78) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
          return 1;
        default:
          break;
      }
    }
    return sub_140FE2700((_DWORD *)a1, a2, a3);
  }
  if ( a2 > 1232036721 )
  {
    if ( a2 <= 1768123488 )
    {
      if ( a2 == 1232036722 )
      {
        *(float *)(a1 + 48) = (*(float (__fastcall **)(__int64 *, __int64 **))(**a3 + 96))(*a3, a3);
        return 1;
      }
      if ( a2 == 1232233827 )
      {
        *(_BYTE *)(a1 + 89) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3);
        return 1;
      }
      if ( a2 != 1232301677 )
        return sub_140FE2700((_DWORD *)a1, a2, a3);
      (*(void (__fastcall **)(__int64 *, _QWORD *, __int64 **))(**a3 + 128))(*a3, v23, a3);
      v6 = (volatile signed __int32 **)(a1 + 32);
LABEL_29:
      if ( v6 != v23 )
      {
        v5 = v23[0];
        v9 = *v6;
        v10 = *v6 - 1;
        if ( *v6 == nullptr )
          v10 = nullptr;
        v11 = (volatile signed __int32 *)(v23[0] - 4LL);
        if ( v23[0] != 0 )
        {
          if ( v9 != nullptr && _InterlockedDecrement(v10) == 0 )
            sub_1412EC9A0(v10, v5);
          *v6 = nullptr;
          _InterlockedIncrement(v11);
          v12 = v11 + 1;
        }
        else
        {
          if ( v9 != nullptr && _InterlockedDecrement(v10) == 0 )
            sub_1412EC9A0(v10, v5);
          v12 = nullptr;
        }
        *v6 = v12;
      }
      v22 = v23[0];
      if ( v23[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v23[0] - 4LL)) == 0 )
        sub_1412EC9A0(v22 - 4, v5);
      return 1;
    }
    switch ( a2 )
    {
      case 1768123489:
        *(_BYTE *)(a1 + 76) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
        return 1;
      case 1768838002:
        *(_BYTE *)(a1 + 84) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
        return 1;
      case 1769169772:
        *(_BYTE *)(a1 + 77) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
        return 1;
      default:
        break;
    }
    return sub_140FE2700((_DWORD *)a1, a2, a3);
  }
  if ( a2 > 1231907183 )
  {
    if ( a2 == 1231907184 )
    {
      *(_BYTE *)(a1 + 80) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
      return 1;
    }
    if ( a2 == 1231908452 )
    {
      *(_WORD *)(a1 + 52) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
      return 1;
    }
    if ( a2 != 1231970669 )
      return sub_140FE2700((_DWORD *)a1, a2, a3);
    (*(void (__fastcall **)(__int64 *, _QWORD *, __int64 **))(**a3 + 128))(*a3, v23, a3);
    v6 = (volatile signed __int32 **)(a1 + 24);
    goto LABEL_29;
  }
  if ( a2 == 1231386724 )
  {
    *(_WORD *)(a1 + 54) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
    return 1;
  }
  if ( a2 == 1231515762 )
  {
    if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
      *(_BYTE *)(a1 + 85) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
    else
      *(_BYTE *)(a1 + 85) = -1;
    return 1;
  }
  if ( a2 != 1231642994 )
    return sub_140FE2700((_DWORD *)a1, a2, a3);
  *(_BYTE *)(a1 + 88) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
  return 1;
}
