__int64 __fastcall sub_140F8F320(int *a1)
{
  int v1; // edx
  int v3; // ebp
  unsigned int v4; // esi
  __int64 v5; // rbx
  __int64 v7; // r14
  _QWORD *v8; // rdx
  __int64 v9; // rax
  __int64 v10; // rdi
  __int64 (__fastcall **v11)(__int64, _QWORD); // rdx
  _QWORD *v12; // r15
  unsigned int v13; // eax
  __int64 *v14; // rsi
  __int64 *v15; // rbx
  __int64 v16; // rax
  __int64 v17; // rcx
  unsigned __int64 v18; // rax
  __int64 v19; // rdx
  __int64 *v20; // r12
  __int64 v21; // rcx
  __int64 v22; // rdx
  __int64 *v23; // rax
  unsigned int v24; // eax
  __int64 v25; // rax
  __int64 v26; // rsi
  __int64 v27; // rcx
  int v28; // ebx
  unsigned int v29; // ebp
  unsigned int v30; // edx
  unsigned int v31; // ebp
  bool v32; // zf
  unsigned int v33; // ecx
  unsigned __int16 v34; // ax
  __int64 v35; // rcx
  __int64 v36; // rax
  __int16 v37; // ax
  char v38; // bp
  unsigned int v39; // eax
  __int64 v40; // rax
  __int64 v41; // rdi
  __int64 v42; // rax
  int v43; // r9d
  int v44; // edi
  __int64 v45; // rsi
  int v46; // r9d
  char v47; // [rsp+37h] [rbp-61h] BYREF
  int v48; // [rsp+38h] [rbp-60h] BYREF
  __int64 v49; // [rsp+40h] [rbp-58h] BYREF
  int v50; // [rsp+48h] [rbp-50h] BYREF
  __int64 v51[9]; // [rsp+50h] [rbp-48h] BYREF

  v1 = *a1 >> 24;
  if ( v1 == -1 )
    return 0;
  v3 = *a1 & 0x7FFFFF;
  v4 = -1;
  if ( v3 == 0x7FFFFF )
  {
    if ( v1 != 53 )
      return 0;
  }
  else
  {
    v4 = *a1 & 0x7FFFFF;
  }
  if ( v1 == 53 )
  {
    v7 = 0;
    if ( v3 != 0x7FFFFF && qword_141B5FE40 != 0 )
    {
      if ( (_BYTE)word_141B60320 != 0 )
      {
        v8 = *(_QWORD **)(qword_141B5FE40 + 128);
        if ( (__int64)(v8[1] - *v8) >> 3 > (unsigned __int64)v4 )
        {
          v7 = *(_QWORD *)(*v8 + 8LL * v4);
          goto LABEL_24;
        }
      }
      else if ( (__int64)(*(_QWORD *)(qword_141B5FE40 + 104) - *(_QWORD *)(qword_141B5FE40 + 96)) >> 3 > (unsigned __int64)v4 )
      {
        v7 = sub_140F5C7E0(v4);
        goto LABEL_24;
      }
      v7 = 0;
    }
LABEL_24:
    v12 = a1 + 2;
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
    if ( (__int64 *)*v12 == &qword_141B5C8A0 )
    {
      v13 = a1[4];
      HIWORD(v48) = v13 >> 17;
      LOWORD(v48) = (v13 >> 8) & 0x1FF | ((_WORD)v13 << 9);
    }
    else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, int *))(*(_QWORD *)*v12 + 8LL))(*v12, a1 + 2) == 27 )
    {
      (*(void (__fastcall **)(_QWORD, __int64 *, int *))(*(_QWORD *)*v12 + 160LL))(*v12, v51, a1 + 2);
      sub_1413CA830(&v48, v51);
    }
    else
    {
      v48 = 124518401;
    }
    v47 = 0;
    if ( (*(unsigned __int8 (__fastcall **)(_QWORD, int *))(*(_QWORD *)*v12 + 8LL))(*v12, a1 + 2) == 10 )
    {
      v14 = nullptr;
      v15 = (__int64 *)(*(__int64 (__fastcall **)(_QWORD, int *, _QWORD))(*(_QWORD *)*v12 + 176LL))(*v12, a1 + 2, 0);
      v16 = *v15;
      v17 = v15[1];
      if ( *v15 != v17 )
      {
        v14 = nullptr;
        while ( *(_DWORD *)v16 != 1182287430 )
        {
          v16 += 16;
          if ( v16 == v17 )
            goto LABEL_42;
        }
        if ( v16 == v17 )
          v14 = nullptr;
        else
          v14 = *(__int64 **)(v16 + 8);
      }
LABEL_42:
      v20 = &qword_141B5A4A0;
      if ( v14 == nullptr )
        v14 = &qword_141B5A4A0;
      if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v14 + 48LL))(*v14, v14) != 0 )
      {
        v21 = *v15;
        v22 = v15[1];
        v23 = nullptr;
        if ( *v15 != v22 )
        {
          while ( *(_DWORD *)v21 != 1719166068 )
          {
            v21 += 16;
            if ( v21 == v22 )
              goto LABEL_54;
          }
          if ( v21 == v22 )
            v23 = nullptr;
          else
            v23 = *(__int64 **)(v21 + 8);
        }
LABEL_54:
        if ( v23 != nullptr )
          v20 = v23;
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
        if ( (__int64 *)*v20 == &qword_141B5C8A0 )
        {
          v24 = *((_DWORD *)v20 + 2);
          WORD1(v49) = v24 >> 17;
          LOWORD(v49) = (v24 >> 8) & 0x1FF | ((_WORD)v24 << 9);
        }
        else if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v20 + 8LL))(*v20, v20) == 27 )
        {
          (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)*v20 + 160LL))(*v20, v51, v20);
          sub_1413CA830(&v49, v51);
        }
        else
        {
          LODWORD(v49) = 124518401;
        }
        v48 = v49;
        v47 = 1;
      }
    }
    v25 = sub_141584930(qword_141B5FE88, v7, (unsigned int)&v48, 0, (__int64)&v47);
    v26 = v25;
    v49 = v25;
    if ( v25 != 0 && (_BYTE)word_141B60320 != 0 )
    {
      v27 = *(_QWORD *)(v25 + 24);
      if ( v27 != 0 && (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v27 + 240LL))(v27) == 0 )
      {
        sub_1414B1E00(v26, v51);
        v28 = LOWORD(v51[0]) >> 9;
        if ( (unsigned __int8)v28 >= 0x50u )
        {
          v29 = 1755;
          if ( (_BYTE)v28 != 127 )
            v29 = 0;
          v30 = (5243 * (v29 >> 2)) >> 17;
          v31 = 15 * ((unsigned __int8)(v29 - 100 * v30 + 5) / 0xFu);
          BYTE1(v28) = 0;
          v32 = (_BYTE)v31 == 60;
          if ( (_BYTE)v31 == 60 )
            LOBYTE(v31) = 0;
          LOBYTE(v28) = v32;
          v33 = (unsigned __int16)(100 * (v30 + v28) + (unsigned __int8)v31);
          LOBYTE(v28) = 0;
          if ( v33 >= 0x258 )
          {
            LOBYTE(v28) = 127;
            if ( v33 != 1755 )
              LOBYTE(v28) = (((unsigned __int16)(137 * ((unsigned __int16)v33 % 0x64u)) >> 11)
                           + 4 * ((5243 * (v33 >> 2)) >> 17)
                           + 105)
                          & 0x7F;
          }
        }
        v34 = v51[0] & 0x1FF;
        if ( WORD1(v51[0]) < HIWORD(dword_141AAE084)
          || WORD1(v51[0]) <= HIWORD(dword_141AAE084)
          && (v34 < (unsigned __int16)(dword_141AAE084 & 0x1FF)
           || v34 <= (unsigned __int16)(dword_141AAE084 & 0x1FF) && (char)v28 < (char)sub_140DB8260(&dword_141AAE084)) )
        {
          sub_1414B16D0(v26);
        }
      }
LABEL_78:
      v35 = *(_QWORD *)(v26 + 24);
      if ( v35 != 0 )
      {
        if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v35 + 240LL))(v35) == 0 )
        {
          v36 = *(_QWORD *)(v26 + 24);
          if ( v36 == 0 )
            goto LABEL_86;
          v37 = *(_WORD *)(v36 + 50);
          if ( (v37 & 1) != 0 && (v37 & 0x3000) != 0 )
            sub_1414B16D0(v26);
        }
        if ( *(_QWORD *)(v26 + 24) != 0 )
          return v26;
      }
LABEL_86:
      v38 = 0;
      if ( (_BYTE)word_141B60320 == 0 )
        return 0;
LABEL_89:
      if ( (*(unsigned __int8 (__fastcall **)(_QWORD, int *))(*(_QWORD *)*v12 + 8LL))(*v12, a1 + 2) != 32 )
        goto LABEL_106;
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
      if ( (__int64 *)*v12 == &qword_141B5C8A0 )
      {
        v39 = a1[4];
        HIWORD(v50) = v39 >> 17;
        LOWORD(v50) = (v39 >> 8) & 0x1FF | ((_WORD)v39 << 9);
      }
      else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, int *))(*(_QWORD *)*v12 + 8LL))(*v12, a1 + 2) == 27 )
      {
        (*(void (__fastcall **)(_QWORD, __int64 *, _QWORD *))(*(_QWORD *)*v12 + 160LL))(*v12, v51, v12);
        sub_1413CA830(&v50, v51);
      }
      else
      {
        v50 = 124518401;
      }
      v48 = v50;
      if ( v7 != 0 && (v40 = sub_1411CF7D0(v7, &v48)) != 0 )
      {
        v41 = v40;
        if ( v38 != 0 )
        {
          v26 = sub_140F84320();
          *(_QWORD *)(v26 + 8) = -1;
          *(_DWORD *)(v26 + 16) = 0;
          *(_QWORD *)v26 = 0x141885608LL;
          *(_QWORD *)(v26 + 24) = 0;
          *(_QWORD *)(v26 + 32) = 0;
          *(_QWORD *)(v26 + 40) = 0;
          *(_BYTE *)(v26 + 48) = 0;
          v49 = v26;
        }
        sub_1414B1AD0(v26, v41);
      }
      else
      {
LABEL_106:
        v5 = 0;
        if ( (HIWORD(v48) ^ 0x76C | v48 & 0x1FF ^ 1) == 0 )
          return v5;
        if ( v7 == 0 )
          return v5;
        v5 = 0;
        v42 = sub_140B4DCD0(v7, (unsigned int)&v48, 0, 0, 0);
        if ( v42 == 0 )
          return v5;
        v44 = v42;
        if ( v38 != 0 )
        {
          v45 = sub_140F84320();
          LOBYTE(v46) = 1;
          sub_1414B1470(v45, v44, v7, v46, 1);
          v49 = v45;
        }
        else
        {
          LOBYTE(v43) = 1;
          sub_1414B15A0(v26, v42, v7, v43, 1);
        }
      }
      sub_141584560(qword_141B5FE88, &v49);
      return v49;
    }
    if ( v25 != 0 )
      goto LABEL_78;
    v38 = 1;
    if ( (_BYTE)word_141B60320 != 0 )
      goto LABEL_89;
    return 0;
  }
  v9 = sub_140F216C0(&qword_141B5FDA8);
  if ( v9 == 0 )
    return 0;
  v10 = v9;
  if ( (_BYTE)word_141B60320 == 0
    && (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v9 + 56LL))(v9) > (unsigned __int64)(int)v4 )
  {
    return sub_140F8FB30(v4, v10);
  }
  v5 = 0;
  if ( (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v10 + 48LL))(v10) <= (unsigned __int64)(int)v4 || v3 == 0x7FFFFF )
    return v5;
  if ( (_BYTE)word_141B60320 == 0 )
  {
    v18 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v10 + 56LL))(v10);
    v19 = *(_QWORD *)v10;
    if ( v18 > v4 )
    {
      v11 = (__int64 (__fastcall **)(__int64, _QWORD))(v19 + 64);
      return (*v11)(v10, v4);
    }
    if ( (*(__int64 (__fastcall **)(__int64))(v19 + 48))(v10) <= (unsigned __int64)v4 )
      return 0;
  }
  v11 = (__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v10 + 16LL);
  return (*v11)(v10, v4);
}
