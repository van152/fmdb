char __fastcall sub_141457140(__int64 a1, int a2, _QWORD *a3)
{
  char result; // al
  __int64 v6; // rbx
  __int64 v7; // rax
  int v8; // eax
  __int64 v9; // rbx
  __int64 v10; // rax
  int v11; // eax
  char v12; // cl
  __int64 v13; // rbx
  __int64 v14; // rax
  int v15; // eax
  __int16 v16; // ax
  __int16 v17; // cx
  char v18; // al
  char v19; // cl
  char v20; // al
  char v21; // cl
  unsigned int v22; // eax
  int v23; // ecx
  int v24; // [rsp+28h] [rbp-30h] BYREF
  _BYTE v25[40]; // [rsp+30h] [rbp-28h] BYREF

  result = 0;
  if ( a2 <= 1886151010 )
  {
    if ( a2 > 1684108388 )
    {
      if ( a2 == 1684108389 )
      {
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
        {
          if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
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
          if ( (__int64 *)*a3 == &qword_141B5C8A0 )
          {
            v22 = *((_DWORD *)a3 + 2);
            HIWORD(v24) = v22 >> 17;
            LOWORD(v24) = (v22 >> 8) & 0x1FF | ((_WORD)v22 << 9);
          }
          else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) == 27 )
          {
            (*(void (__fastcall **)(_QWORD, _BYTE *, _QWORD *))(*(_QWORD *)*a3 + 160LL))(*a3, v25, a3);
            sub_1413CA830(&v24, v25);
          }
          else
          {
            v24 = 124518401;
          }
          v23 = v24;
          *(_DWORD *)(a1 + 36) = v24;
          result = 1;
          if ( (v23 & 0x1FF) == 1 && (v23 & 0xFFFF0000) == 0x76C0000 )
          {
            *(_WORD *)(a1 + 38) = 2000;
            *(_WORD *)(a1 + 36) = v23 & 0xFE00 | 1;
          }
        }
        else
        {
          *(_DWORD *)(a1 + 36) = 124518401;
          return 1;
        }
      }
      else if ( a2 == 1869899105 )
      {
        v13 = qword_141B5FE40;
        sub_140FE7960(v25, a3, 1416914273);
        v14 = sub_140FA3700(v13, v25);
        if ( v14 != 0 )
          v15 = *(_DWORD *)(v14 + 12);
        else
          v15 = -1;
        *(_DWORD *)(a1 + 40) = v15;
        return 1;
      }
    }
    else if ( a2 == 1634365282 )
    {
      if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
      {
        v20 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 80LL))(*a3, a3);
        v21 = 1;
        if ( (unsigned __int8)v20 >= 2u )
          v21 = v20;
        *(_BYTE *)(a1 + 45) = v21;
        return 1;
      }
      else
      {
        *(_BYTE *)(a1 + 45) = 0;
        return 1;
      }
    }
    else if ( a2 == 1668246896 )
    {
      v9 = qword_141B5FDC0;
      sub_140FE7960(v25, a3, 1668246896);
      v10 = sub_140F7A940(v9, v25);
      if ( v10 != 0 )
        v11 = *(_DWORD *)(v10 + 12);
      else
        v11 = -1;
      *(_DWORD *)(a1 + 32) = v11;
      return 1;
    }
  }
  else if ( a2 <= 1952801132 )
  {
    if ( a2 == 1886151011 )
    {
      *(_BYTE *)(a1 + 44) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      return 1;
    }
    if ( a2 == 1886547821 )
    {
      v12 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3) | *(_BYTE *)(a1 + 46) & 0xFE;
      goto LABEL_37;
    }
  }
  else
  {
    if ( a2 != 2036687218 )
    {
      if ( a2 != 2003267699 )
      {
        if ( a2 == 1952801133 )
        {
          v6 = qword_141B5FE40;
          sub_140FE7960(v25, a3, 1416914273);
          v7 = sub_140FA3700(v6, v25);
          if ( v7 != 0 )
            v8 = *(_DWORD *)(v7 + 12);
          else
            v8 = -1;
          *(_DWORD *)(a1 + 28) = v8;
          return 1;
        }
        return result;
      }
      v18 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
      v19 = *(_BYTE *)(a1 + 46);
      if ( v18 != 0 )
        v12 = v19 | 4;
      else
        v12 = v19 & 0xFB;
LABEL_37:
      *(_BYTE *)(a1 + 46) = v12;
      return 1;
    }
    if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
    {
      v16 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 80LL))(*a3, a3);
      *(_WORD *)(a1 + 36) &= 0xFE00u;
      v17 = 2000;
      if ( v16 != 1900 )
        v17 = v16;
      *(_WORD *)(a1 + 38) = v17;
      return 1;
    }
    else
    {
      *(_WORD *)(a1 + 36) &= 0xFE00u;
      *(_WORD *)(a1 + 38) = 1900;
      return 1;
    }
  }
  return result;
}
