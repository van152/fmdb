__int64 __fastcall sub_141586A80(__int64 a1, __int64 a2, _QWORD *a3)
{
  __int64 v3; // rbx
  _QWORD *v4; // rdi
  __int64 v5; // rax
  __int64 v6; // rsi
  __int64 v7; // rax
  __int64 v8; // rsi
  unsigned __int64 v9; // rcx
  __int64 v10; // rax
  __int64 v11; // rdi
  __int64 v12; // rdi
  bool v13; // al
  __int64 *v15; // [rsp+20h] [rbp-58h] BYREF
  _QWORD *v16; // [rsp+28h] [rbp-50h]
  __int64 v17; // [rsp+30h] [rbp-48h] BYREF
  char v18; // [rsp+38h] [rbp-40h]
  _QWORD v19[2]; // [rsp+40h] [rbp-38h] BYREF
  __int64 v20; // [rsp+50h] [rbp-28h]

  v4 = a3;
  v5 = -*(_DWORD *)(a1 - 4);
  v6 = a1 + v5;
  if ( (int)a2 > 1332110958 )
  {
    if ( (int)a2 > 1332897125 )
    {
      if ( (int)a2 > 1332901229 )
      {
        if ( (_DWORD)a2 == 1332901230 )
        {
          *(_BYTE *)(v6 - 17) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(a1: *a3, a2: a3);
        }
        else
        {
          if ( (_DWORD)a2 != 1333029744 )
            return sub_140DFF760(a1: v6 - 192, a2, a3);
          *(_BYTE *)(v6 - 16) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(a1: *a3, a2: a3);
        }
      }
      else if ( (_DWORD)a2 == 1332897126 )
      {
        *(_BYTE *)(v6 - 18) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(a1: *a3, a2: a3);
      }
      else
      {
        if ( (_DWORD)a2 != 1332897136 )
          return sub_140DFF760(a1: v6 - 192, a2, a3);
        *(_WORD *)(v6 - 24) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(a1: *a3, a2: a3);
      }
    }
    else if ( (int)a2 > 1332769394 )
    {
      if ( (_DWORD)a2 == 1332769395 )
      {
        *(_BYTE *)(v6 - 19) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(a1: *a3, a2: a3);
      }
      else
      {
        if ( (_DWORD)a2 != 1332769889 )
          return sub_140DFF760(a1: v6 - 192, a2, a3);
        *(_WORD *)(v6 - 26) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(a1: *a3, a2: a3);
      }
    }
    else if ( (_DWORD)a2 == 1332110959 )
    {
      *(_BYTE *)(v6 - 15) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(a1: *a3, a2: a3);
    }
    else
    {
      if ( (_DWORD)a2 != 1332309357 )
        return sub_140DFF760(a1: v6 - 192, a2, a3);
      *(_BYTE *)(v6 - 20) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(a1: *a3, a2: a3);
    }
    goto LABEL_52;
  }
  if ( (int)a2 > 1331917408 )
  {
    if ( (int)a2 > 1331980658 )
    {
      if ( (_DWORD)a2 == 1331980659 )
      {
        *(_BYTE *)(v6 - 21) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(a1: *a3, a2: a3);
      }
      else
      {
        if ( (_DWORD)a2 != 1332106563 )
          return sub_140DFF760(a1: v6 - 192, a2, a3);
        *(_BYTE *)(v6 - 13) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(a1: *a3, a2: a3);
      }
    }
    else if ( (_DWORD)a2 == 1331917409 )
    {
      *(_WORD *)(v6 - 28) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(a1: *a3, a2: a3);
    }
    else
    {
      if ( (_DWORD)a2 != 1331917929 )
        return sub_140DFF760(a1: v6 - 192, a2, a3);
      v3 = qword_141B5FDB0;
      sub_140FE7960(a1: &v17, a2: a3, a3: 1667855481);
      *(_QWORD *)(v6 - 200) = sub_140FA3700(a1: v3, a2: &v17);
    }
    goto LABEL_52;
  }
  v7 = a1 + v5 - 312;
  if ( (int)a2 <= 1331913073 )
  {
    if ( (_DWORD)a2 != 1331784806 )
    {
      if ( (_DWORD)a2 == 1331913057 )
      {
        v17 = v7;
        v18 = 0;
        sub_1417354D0(a1: v19, a2: v7, a3: 0);
        v15 = &v17;
        v16 = v19;
        LODWORD(v3) = sub_14158A330(a1: &v15, a2: v4);
        v8 = v19[0];
        if ( v19[0] != 0 )
        {
          v9 = v20 - v19[0];
          v10 = qword_141ABD470;
          if ( v20 - v19[0] == -1 )
            v9 = *(unsigned int *)(v19[0] - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
          {
LABEL_48:
            MEMORY[0x141948990](a1: v8 - *(unsigned int *)(v10 + 48));
            return (unsigned int)v3;
          }
LABEL_44:
          v11 = *(_QWORD *)(v10 + 24);
          if ( (*(_QWORD *)(v10 + 32) - v11) >> 3 > v9 )
          {
            v12 = *(_QWORD *)(v11 + 8 * v9);
            if ( v12 != 0 )
            {
              MEMORY[0x1419475D8](a1: v12 + 32, a2: v8 - *(unsigned int *)(v12 + 120));
              v13 = *(_BYTE *)(v12 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v12 + 64)) != 0;
              if ( !v13 && *(_BYTE *)(v12 + 97) != 0 )
                sub_1412D33C0(a1: v12);
              return (unsigned int)v3;
            }
          }
          goto LABEL_48;
        }
        return (unsigned int)v3;
      }
      return sub_140DFF760(a1: v6 - 192, a2, a3);
    }
    *(_BYTE *)(v6 - 22) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(a1: *a3, a2: a3);
LABEL_52:
    LOBYTE(v3) = 1;
    return (unsigned int)v3;
  }
  if ( (_DWORD)a2 == 1331913074 )
  {
    v17 = v7;
    v18 = 1;
    LOBYTE(a3) = 1;
    sub_1417354D0(a1: v19, a2: v7, a3);
    v15 = &v17;
    v16 = v19;
    LODWORD(v3) = sub_14158A330(a1: &v15, a2: v4);
    v8 = v19[0];
    if ( v19[0] != 0 )
    {
      v9 = v20 - v19[0];
      v10 = qword_141ABD470;
      if ( v20 - v19[0] == -1 )
        v9 = *(unsigned int *)(v19[0] - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_48;
      goto LABEL_44;
    }
    return (unsigned int)v3;
  }
  if ( (_DWORD)a2 == 1331916399 )
  {
    *(_BYTE *)(v6 - 14) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(a1: *a3, a2: a3);
    goto LABEL_52;
  }
  return sub_140DFF760(a1: v6 - 192, a2, a3);
}
