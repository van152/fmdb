char __fastcall sub_140FEB670(__int64 a1, __int64 a2)
{
  char result; // al
  _QWORD *v5; // rdi
  __int64 v6; // rcx
  _QWORD *v7; // rsi
  char v8; // r14
  __int64 *v9; // rbp
  __int64 *v10; // rax
  __int64 v11; // rcx
  __int64 v12; // rax
  __int64 *v13; // rdx
  __int64 v14; // rcx
  __int64 *v15; // rbp
  __int64 *v16; // rax
  __int64 v17; // rcx
  __int64 v18; // rax
  __int64 *v19; // rdx
  unsigned int v20; // eax
  int v21; // eax
  int v22; // ecx
  int v23; // [rsp+28h] [rbp-40h] BYREF
  int v24; // [rsp+30h] [rbp-38h] BYREF
  __int64 v25[6]; // [rsp+38h] [rbp-30h] BYREF

  if ( *(_DWORD *)a2 != *(_DWORD *)a1 )
    return 0;
  result = 1;
  if ( (*(_DWORD *)a2 & 0xFF000000) != 0x35000000 )
    return result;
  v5 = (_QWORD *)(a1 + 8);
  if ( (*(unsigned __int8 (__fastcall **)(_QWORD, __int64))(**(_QWORD **)(a1 + 8) + 8LL))(*(_QWORD *)(a1 + 8), a1 + 8) == 32 )
  {
    v6 = *(_QWORD *)(a2 + 8);
    v7 = (_QWORD *)(a2 + 8);
    v8 = 1;
    if ( (*(unsigned __int8 (__fastcall **)(__int64, _QWORD *))(*(_QWORD *)v6 + 8LL))(v6, v7) != 32 )
      goto LABEL_20;
  }
  else
  {
    v9 = nullptr;
    v10 = (__int64 *)(*(__int64 (__fastcall **)(_QWORD, __int64, _QWORD))(*(_QWORD *)*v5 + 176LL))(*v5, a1 + 8, 0);
    v11 = *v10;
    v12 = v10[1];
    if ( v11 != v12 )
    {
      v9 = nullptr;
      while ( *(_DWORD *)v11 != 1182287430 )
      {
        v11 += 16;
        if ( v11 == v12 )
          goto LABEL_14;
      }
      if ( v11 == v12 )
        v9 = nullptr;
      else
        v9 = *(__int64 **)(v11 + 8);
    }
LABEL_14:
    v13 = &qword_141B5A4A0;
    if ( v9 != nullptr )
      v13 = v9;
    v8 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v13 + 48LL))(*v13);
    v14 = *(_QWORD *)(a2 + 8);
    v7 = (_QWORD *)(a2 + 8);
    if ( (*(unsigned __int8 (__fastcall **)(__int64, _QWORD *))(*(_QWORD *)v14 + 8LL))(v14, v7) != 32 )
    {
LABEL_20:
      v15 = nullptr;
      v16 = (__int64 *)(*(__int64 (__fastcall **)(_QWORD, _QWORD *, _QWORD))(*(_QWORD *)*v7 + 176LL))(*v7, v7, 0);
      v17 = *v16;
      v18 = v16[1];
      if ( v17 != v18 )
      {
        v15 = nullptr;
        while ( *(_DWORD *)v17 != 1182287430 )
        {
          v17 += 16;
          if ( v17 == v18 )
            goto LABEL_28;
        }
        if ( v17 == v18 )
          v15 = nullptr;
        else
          v15 = *(__int64 **)(v17 + 8);
      }
LABEL_28:
      v19 = &qword_141B5A4A0;
      if ( v15 != nullptr )
        v19 = v15;
      if ( v8 == (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v19 + 48LL))(*v19) )
        goto LABEL_31;
      return 0;
    }
    if ( v8 == 0 )
      return 0;
  }
LABEL_31:
  if ( (*(unsigned __int8 (__fastcall **)(_QWORD, __int64))(*(_QWORD *)*v5 + 8LL))(*v5, a1 + 8) != 32
    || (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*v7 + 8LL))(*v7, v7) != 32 )
  {
    return (*(__int64 (__fastcall **)(_QWORD, __int64, _QWORD *))(*(_QWORD *)*v5 + 8LL * (*v5 != *v7) + 32))(
             *v5,
             a1 + 8,
             v7);
  }
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
  if ( (__int64 *)*v5 == &qword_141B5C8A0 )
  {
    v20 = *(_DWORD *)(a1 + 16);
    HIWORD(v23) = v20 >> 17;
    LOWORD(v23) = (v20 >> 8) & 0x1FF | ((_WORD)v20 << 9);
  }
  else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, __int64))(*(_QWORD *)*v5 + 8LL))(*v5, a1 + 8) == 27 )
  {
    (*(void (__fastcall **)(_QWORD, __int64 *, _QWORD *))(*(_QWORD *)*v5 + 160LL))(*v5, v25, v5);
    sub_1413CA830(&v23, v25);
  }
  else
  {
    v23 = 124518401;
  }
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
  if ( (__int64 *)*v7 == &qword_141B5C8A0 )
  {
    v22 = *((_DWORD *)v7 + 2) >> 17;
    v21 = (*((_DWORD *)v7 + 2) >> 8) & 0x1FF | (*((_DWORD *)v7 + 2) << 9);
  }
  else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*v7 + 8LL))(*v7, v7) == 27 )
  {
    (*(void (__fastcall **)(_QWORD, __int64 *, _QWORD *))(*(_QWORD *)*v7 + 160LL))(*v7, v25, v7);
    sub_1413CA830(&v24, v25);
    LOWORD(v21) = v24;
    LOWORD(v22) = HIWORD(v24);
  }
  else
  {
    LOWORD(v21) = 1;
    LOWORD(v22) = 1900;
  }
  return (((unsigned __int16)v23 ^ (unsigned __int16)v21) & 0x1FF | (unsigned __int16)(HIWORD(v23) ^ v22)) == 0;
}
