bool __fastcall sub_140F82F50(__int64 a1, __int64 a2)
{
  __int64 v3; // rdi
  _DWORD *v4; // rbx
  int v5; // eax
  _DWORD *v6; // rbx
  int v7; // ecx
  char v8; // al
  int v9; // ecx
  __int64 v10; // rdx
  __int64 v11; // rax
  __int64 v12; // rax
  __int64 *v13; // rdx
  __int64 v14; // r8
  _DWORD *v16; // rbx
  _DWORD *v17; // rbx
  int v18; // eax
  __int64 v19; // rax
  unsigned __int16 v20; // cx
  __int64 v21; // r8
  __int64 v22; // rax
  __int64 v23; // rcx
  __int64 v24; // rcx
  __int64 v25; // rcx
  _DWORD *v26; // rdi
  __int64 v27; // rcx
  __int64 v28; // rcx
  __int64 v29; // rcx
  char v30; // [rsp+26h] [rbp-72h] BYREF
  char v31; // [rsp+27h] [rbp-71h] BYREF
  __int64 v32; // [rsp+28h] [rbp-70h] BYREF
  char v33; // [rsp+30h] [rbp-68h]
  __int64 v34; // [rsp+38h] [rbp-60h] BYREF
  __int64 v35; // [rsp+40h] [rbp-58h]
  __int64 v36; // [rsp+48h] [rbp-50h]
  __int64 v37; // [rsp+50h] [rbp-48h]

  v3 = a1;
  v4 = *(_DWORD **)a2;
  if ( (*(_BYTE *)(*(_QWORD *)a2 + 12LL) & 2) != 0 && WORD2(qword_141B6034C) != 0 )
  {
    if ( a1 != 0 )
    {
      v9 = *(_DWORD *)(a1 + 8);
      v10 = v9;
    }
    else
    {
      v9 = -1;
      v10 = -1;
    }
    v34 = v10;
    if ( BYTE5(qword_141B6034C) != 0 && byte_141B5FC2C == 0 )
    {
      v12 = *(_QWORD *)v4;
      v13 = &v34;
      v14 = 8;
      goto LABEL_26;
    }
    LODWORD(v32) = v9;
    v12 = *(_QWORD *)v4;
    v13 = &v32;
LABEL_25:
    v14 = 4;
LABEL_26:
    (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(v12 + 40))(v4, v13, v14);
    return v4[4] == 0;
  }
  if ( a1 == 0 )
  {
LABEL_19:
    LODWORD(v34) = -1;
    v12 = *(_QWORD *)v4;
    v13 = &v34;
    goto LABEL_25;
  }
  v5 = *(_DWORD *)(a1 + 8);
  if ( v5 == -1 )
  {
    if ( (_BYTE)word_141B60320 != 0 && *(_DWORD *)(a1 + 12) != -1 )
    {
      v11 = sub_1400568B0(qword_141B5FE10);
      v4 = *(_DWORD **)a2;
      if ( v11 != 0 )
      {
        v3 = v11;
        v5 = *(_DWORD *)(v11 + 8);
        goto LABEL_5;
      }
    }
    goto LABEL_19;
  }
LABEL_5:
  LODWORD(v34) = v5;
  (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v4 + 40LL))(v4, &v34, 4);
  if ( v4[4] != 0 )
    return false;
  if ( (_BYTE)word_141B60320 != 0 && (*(_BYTE *)(*(_QWORD *)a2 + 12LL) & 2) == 0 )
  {
    if ( (unsigned __int8)sub_141088330(v3) != 0 )
      *(_BYTE *)(v3 + 26) |= 2u;
    sub_141088560(v3);
    *(_QWORD *)(v3 + 24) = *(_QWORD *)(v3 + 24) & 0xFFFFFFFFEFFFFFFFuLL
                         | ((unsigned __int64)((*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v3 + 528LL))(v3)
                                             ^ 1u) << 28);
    *(_QWORD *)(v3 + 24) = *(_QWORD *)(v3 + 24) & 0xFFFFFFFFFFFFFEFFuLL
                         | ((unsigned __int64)((*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v3 + 208LL))(v3)
                                             ^ 1u) << 8);
    *(_QWORD *)(v3 + 24) = *(_QWORD *)(v3 + 24) & 0xFFFFFFFFFFFFFDFFuLL
                         | ((unsigned __int64)(*(unsigned __int8 (__fastcall **)(__int64, __int64))(*(_QWORD *)qword_141B5F278
                                                                                                  + 88LL))(
                                                qword_141B5F278,
                                                v3) << 9);
  }
  v6 = *(_DWORD **)a2;
  v7 = *(_DWORD *)(*(_QWORD *)a2 + 12LL);
  if ( byte_141AAE088 != 0 )
    v8 = (2 * ~(_BYTE)v7) & 4;
  else
    v8 = 0;
  v30 = v8;
  if ( (v7 & 2) == 0 )
  {
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v6 + 40LL))(v6, &v30, 1);
    if ( v6[4] != 0 )
      return false;
    v8 = v30;
  }
  if ( v8 != 0 )
  {
    v16 = *(_DWORD **)a2;
    LODWORD(v34) = *(_DWORD *)(v3 + 12);
    (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v16 + 40LL))(v16, &v34, 4);
    if ( v16[4] == 0 )
    {
      v17 = *(_DWORD **)a2;
      v18 = *(_DWORD *)(v3 + 16);
      if ( v18 == 0 )
        v18 = *(_DWORD *)(v3 + 12);
      LODWORD(v34) = v18;
      (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v17 + 40LL))(v17, &v34, 4);
      if ( v17[4] == 0 )
      {
        v32 = v3;
        v33 = 0;
        v19 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v3 + 1840LL))(v3);
        if ( v19 != 0 )
        {
          v20 = *(_WORD *)(v19 + 30);
          v33 = v20 >> 7;
          *(_WORD *)(v19 + 30) = v20 & 0xFF7F;
        }
        sub_140F855C0(&v34, v3);
        LOBYTE(v21) = 1;
        if ( (unsigned __int8)sub_14132D800(&v34, a2, v21) != 0 )
        {
          if ( (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v3 + 496LL))(v3) != 0 )
          {
            v22 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v3 + 496LL))(v3);
            if ( (unsigned __int8)sub_141457730(v22, a2) != 0 )
            {
LABEL_42:
              v23 = v37;
              if ( v37 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v37 - 4)) == 0 )
                sub_1412EC9A0(v23 - 4);
              v24 = v36;
              if ( v36 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v36 - 4)) == 0 )
                sub_1412EC9A0(v24 - 4);
              v25 = v35;
              if ( v35 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v35 - 4)) == 0 )
                sub_1412EC9A0(v25 - 4);
              sub_14157C630(&v32);
              return true;
            }
          }
          else
          {
            v26 = *(_DWORD **)a2;
            v31 = 0;
            (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v26 + 40LL))(v26, &v31, 1);
            if ( v26[4] == 0 && *(_DWORD *)(*(_QWORD *)a2 + 16LL) == 0 )
              goto LABEL_42;
          }
        }
        v27 = v37;
        if ( v37 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v37 - 4)) == 0 )
          sub_1412EC9A0(v27 - 4);
        v28 = v36;
        if ( v36 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v36 - 4)) == 0 )
          sub_1412EC9A0(v28 - 4);
        v29 = v35;
        if ( v35 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v35 - 4)) == 0 )
          sub_1412EC9A0(v29 - 4);
        sub_14157C630(&v32);
      }
    }
    return false;
  }
  return true;
}
