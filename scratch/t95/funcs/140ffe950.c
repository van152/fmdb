char __fastcall sub_140FFE950(__int64 a1, int a2, __int64 **a3)
{
  __int64 v5; // rdx
  volatile signed __int32 **v6; // rsi
  __int64 v7; // rsi
  __int64 v8; // rax
  __int64 v9; // rdi
  __int64 i; // rbx
  __int64 v11; // rbx
  __int64 v12; // rbx
  __int64 v14; // rbx
  __int64 v15; // rbx
  volatile signed __int32 *v16; // rax
  volatile signed __int32 *v17; // rcx
  volatile signed __int32 *v18; // rdi
  volatile signed __int32 *v19; // rdi
  __int64 v20; // rcx
  unsigned int v21; // eax
  __int64 v22; // [rsp+28h] [rbp-30h] BYREF
  int v23; // [rsp+30h] [rbp-28h] BYREF

  if ( a2 <= 1147563360 )
  {
    if ( a2 <= 1147235948 )
    {
      if ( a2 > 1144091766 )
      {
        if ( a2 == 1144091767 )
        {
          if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
            *(_WORD *)(a1 + 112) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
          else
            *(_WORD *)(a1 + 112) = -1;
          return 1;
        }
        if ( a2 == 1145392197 )
        {
          sub_140FAF0A0(qword_141B5FE58, *(unsigned int *)(a1 + 8));
          v7 = qword_141B5FE58;
          v8 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5FE58 + 48LL))(qword_141B5FE58);
          if ( v8 != 0 )
          {
            v9 = v8;
            for ( i = 0; i != v9; ++i )
              *(_DWORD *)((*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v7 + 16LL))(v7, (unsigned int)i) + 8) = i;
          }
          return 1;
        }
      }
      else
      {
        if ( a2 == 1144091748 )
        {
          if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
            *(_WORD *)(a1 + 114) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
          else
            *(_WORD *)(a1 + 114) = -1;
          return 1;
        }
        if ( a2 == 1144091756 )
        {
          if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
            *(_WORD *)(a1 + 116) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
          else
            *(_WORD *)(a1 + 116) = -1;
          return 1;
        }
      }
      return sub_140FE2700((_DWORD *)a1, a2, a3);
    }
    if ( a2 > 1147561776 )
    {
      if ( a2 == 1147561777 )
      {
        if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
          *(_BYTE *)(a1 + 118) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
        else
          *(_BYTE *)(a1 + 118) = -1;
        return 1;
      }
      if ( a2 == 1147561778 )
      {
        if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
          *(_BYTE *)(a1 + 119) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
        else
          *(_BYTE *)(a1 + 119) = -1;
        return 1;
      }
      return sub_140FE2700((_DWORD *)a1, a2, a3);
    }
    if ( a2 == 1147235949 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 *, __int64 **))(**a3 + 128))(*a3, &v22, a3);
      v6 = (volatile signed __int32 **)(a1 + 48);
    }
    else
    {
      if ( a2 != 1147237230 )
        return sub_140FE2700((_DWORD *)a1, a2, a3);
      (*(void (__fastcall **)(__int64 *, __int64 *, __int64 **))(**a3 + 128))(*a3, &v22, a3);
      v6 = (volatile signed __int32 **)(a1 + 40);
    }
    goto LABEL_48;
  }
  if ( a2 <= 1148089457 )
  {
    switch ( a2 )
    {
      case 1147563361:
        if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
          *(_DWORD *)(a1 + 100) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
        else
          *(_DWORD *)(a1 + 100) = -1;
        return 1;
      case 1147563362:
      case 1147563365:
      case 1147563366:
      case 1147563367:
      case 1147563368:
      case 1147563369:
      case 1147563370:
      case 1147563371:
      case 1147563372:
      case 1147563373:
      case 1147563374:
      case 1147563375:
      case 1147563376:
      case 1147563377:
      case 1147563378:
        return sub_140FE2700((_DWORD *)a1, a2, a3);
      case 1147563363:
        v11 = qword_141B5FDC0;
        sub_140FE7960(&v22, a3, 1668246896);
        *(_QWORD *)(a1 + 80) = sub_140F7A940(v11, &v22);
        return 1;
      case 1147563364:
        if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(&dword_141B5C8D0);
          if ( dword_141B5C8D0 == -1 )
          {
            sub_140DBC9B0(&qword_141B5C8A0);
            sub_141751048(sub_140DBCA10);
            sub_141750EA0(&dword_141B5C8D0);
          }
        }
        if ( *a3 == &qword_141B5C8A0 )
        {
          v21 = *((_DWORD *)a3 + 2);
          HIWORD(v23) = v21 >> 17;
          LOWORD(v23) = (v21 >> 8) & 0x1FF | ((_WORD)v21 << 9);
        }
        else if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) == 27 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 *, __int64 **))(**a3 + 160))(*a3, &v22, a3);
          sub_1413CA830(&v23, &v22);
        }
        else
        {
          v23 = 124518401;
        }
        *(_DWORD *)(a1 + 96) = v23;
        return 1;
      case 1147563379:
        v12 = qword_141B5FE28;
        sub_140FE7960(&v22, a3, 1937006948);
        *(_QWORD *)(a1 + 88) = sub_140F7A940(v12, &v22);
        return 1;
      default:
        if ( a2 != 1148084589 )
          return sub_140FE2700((_DWORD *)a1, a2, a3);
        (*(void (__fastcall **)(__int64 *, __int64 *, __int64 **))(**a3 + 128))(*a3, &v22, a3);
        v6 = (volatile signed __int32 **)(a1 + 24);
        break;
    }
    goto LABEL_48;
  }
  if ( a2 <= 1148480816 )
  {
    if ( a2 == 1148089458 )
    {
      *(_BYTE *)(a1 + 125) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 80))(*a3, a3);
      return 1;
    }
    if ( a2 != 1148415597 )
      return sub_140FE2700((_DWORD *)a1, a2, a3);
    (*(void (__fastcall **)(__int64 *, __int64 *, __int64 **))(**a3 + 128))(*a3, &v22, a3);
    v6 = (volatile signed __int32 **)(a1 + 32);
LABEL_48:
    if ( v6 != (volatile signed __int32 **)&v22 )
    {
      v5 = v22;
      v16 = *v6;
      v17 = *v6 - 1;
      if ( *v6 == nullptr )
        v17 = nullptr;
      v18 = (volatile signed __int32 *)(v22 - 4);
      if ( v22 != 0 )
      {
        if ( v16 != nullptr && _InterlockedDecrement(v17) == 0 )
          sub_1412EC9A0(v17, v5);
        *v6 = nullptr;
        _InterlockedIncrement(v18);
        v19 = v18 + 1;
      }
      else
      {
        if ( v16 != nullptr && _InterlockedDecrement(v17) == 0 )
          sub_1412EC9A0(v17, v5);
        v19 = nullptr;
      }
      *v6 = v19;
    }
    v20 = v22;
    if ( v22 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v22 - 4)) == 0 )
      sub_1412EC9A0(v20 - 4, v5);
    return 1;
  }
  if ( a2 == 1148480817 )
  {
    v14 = qword_141B5FE40;
    sub_140FE7960(&v22, a3, 1416914273);
    *(_QWORD *)(a1 + 64) = sub_140FA3700(v14, &v22);
    return 1;
  }
  if ( a2 == 1148480818 )
  {
    v15 = qword_141B5FE40;
    sub_140FE7960(&v22, a3, 1416914273);
    *(_QWORD *)(a1 + 72) = sub_140FA3700(v15, &v22);
    return 1;
  }
  if ( a2 != 1148675186 )
    return sub_140FE2700((_DWORD *)a1, a2, a3);
  *(_BYTE *)(a1 + 124) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 80))(*a3, a3);
  return 1;
}
