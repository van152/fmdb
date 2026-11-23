__int64 __fastcall sub_1411BB2F0(__int64 a1, _WORD *a2, _WORD *a3, __int64 a4, char a5)
{
  signed int v5; // ebp
  __int64 v7; // r12
  __int64 v8; // r13
  __int16 v9; // r14
  __int16 v10; // r15
  __int64 v11; // rax
  __int64 v12; // rcx
  __int64 v13; // rcx
  _QWORD *v14; // rbx
  __int64 v15; // rcx
  __int64 v16; // rax
  __int64 v17; // rdi
  __int64 v18; // rcx
  __int64 v19; // rcx
  __int64 v20; // rax
  __int64 v21; // rbx
  unsigned __int8 v22; // al
  int v23; // ecx
  __int16 v24; // r9
  __int16 v25; // r8
  __int16 v26; // si
  __int16 v27; // ax
  int v28; // edx
  int v29; // ebx
  _WORD *v30; // r14
  __int64 v31; // rdi
  __int64 v32; // rcx
  char v33; // dl
  __int16 v35; // [rsp+34h] [rbp-64h]
  int v36; // [rsp+38h] [rbp-60h]
  __int16 v37; // [rsp+3Ch] [rbp-5Ch]

  if ( *(_BYTE *)(a1 + 40) != 0 && *(_BYTE *)(a1 + 47) != 1 )
    return 0;
  *a2 = 0;
  *a3 = 0;
  v7 = *(_QWORD *)(a1 + 56);
  v8 = *(_QWORD *)(a1 + 64);
  LOBYTE(v5) = 4;
  if ( v7 != v8 )
  {
    v9 = 0;
    v10 = 0;
    v35 = 0;
    v36 = 0;
    v37 = 0;
    do
    {
      v14 = *(_QWORD **)v7;
      v15 = *(_QWORD *)v7 + *(int *)(*(_QWORD *)(*(_QWORD *)v7 + 8LL) + 4LL) + 8LL;
      v16 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v15 + 1728LL))(v15);
      if ( v16 != 0 )
      {
        v17 = v16;
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD *))(*v14 + 640LL))(v14) == 0
          && (*(unsigned __int8 (__fastcall **)(_QWORD *))(*v14 + 664LL))(v14) == 0 )
        {
          v18 = (__int64)v14 + *(int *)(v14[1] + 4LL) + 8;
          if ( (*(unsigned __int8 (__fastcall **)(__int64, _QWORD, _QWORD, _QWORD, _QWORD, _QWORD))(*(_QWORD *)v18
                                                                                                  + 1384LL))(
                 v18,
                 0,
                 0,
                 0,
                 0,
                 0) == 0 )
          {
            if ( *(_BYTE *)(a1 + 47) == 1
              || (*(char (__fastcall **)(_QWORD *))(*v14 + 1104LL))(v14) >= 30
              && (*(_BYTE *)(a1 + 47) == 1
               || (v19 = v17 + *(int *)(*(_QWORD *)(v17 + 8) + 4LL) + 8,
                   (v20 = (*(__int64 (__fastcall **)(__int64, _QWORD, _QWORD))(*(_QWORD *)v19 + 1024LL))(
                            v19,
                            *(_QWORD *)(a1 + 48),
                            0)) != 0)
               && (v21 = v20, (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v20 + 136LL))(v20) != 5)
               && (v22 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v21 + 248LL))(v21)) <= 0x15u
               && (v23 = 4162558, _bittest(&v23, v22))) )
            {
              v11 = *(_QWORD *)(v17 + 8);
              v12 = *(int *)(v11 + 8);
              v10 += 10 * *(char *)(v12 + v17 + 90);
              v35 += 10 * *(char *)(v12 + v17 + 89);
              v13 = v17 + *(int *)(v11 + 4) + 8;
              v36 += 10 * (*(char (__fastcall **)(__int64))(*(_QWORD *)v13 + 1488LL))(v13);
              v37 += 10 * *(char *)(*(int *)(*(_QWORD *)(v17 + 8) + 8LL) + v17 + 92);
              ++v9;
            }
          }
        }
      }
      v7 += 8;
    }
    while ( v7 != v8 );
    if ( v9 != 0 )
    {
      v24 = v10 / v9;
      v25 = v35 / v9;
      v26 = (__int16)v36 / v9;
      v27 = v37 / v9;
      v28 = (__int16)((__int16)v36 / v9);
      v5 = (__int16)(v10 / v9);
      v29 = (__int16)(v35 / v9);
      if ( a5 != 0 )
      {
        v30 = a2;
        v31 = a4;
        if ( v28 < v5 && v28 < v29 && v28 < v27 )
        {
          if ( a4 == 0 )
          {
LABEL_26:
            LOBYTE(v5) = 2;
LABEL_52:
            *v30 = v26;
            return (unsigned int)v5;
          }
          goto LABEL_31;
        }
        if ( v5 >= v28 || v5 >= v29 || v5 >= v27 )
        {
          if ( v29 >= v5 || v29 >= v28 || v29 >= v27 )
          {
LABEL_49:
            if ( v31 == 0 )
            {
              LOBYTE(v5) = 1;
              v26 = v27;
              goto LABEL_52;
            }
            v33 = *(_BYTE *)(*(int *)(*(_QWORD *)(v31 + 8) + 8LL) + v31 + 92);
            LOBYTE(v5) = 1;
            v26 = v27;
            goto LABEL_51;
          }
LABEL_47:
          if ( v31 == 0 )
          {
            LOBYTE(v5) = 10;
            v26 = v25;
            goto LABEL_52;
          }
          v33 = *(_BYTE *)(*(int *)(*(_QWORD *)(v31 + 8) + 8LL) + v31 + 89);
          LOBYTE(v5) = 10;
          v26 = v25;
          goto LABEL_51;
        }
      }
      else
      {
        v30 = a2;
        v31 = a4;
        if ( v28 > v5 && v28 > v29 && v28 > v27 )
        {
          if ( a4 == 0 )
            goto LABEL_26;
LABEL_31:
          v32 = v31 + *(int *)(*(_QWORD *)(v31 + 8) + 4LL) + 8;
          v33 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v32 + 1488LL))(v32);
          LOBYTE(v5) = 2;
LABEL_51:
          *a3 = 10 * v33;
          goto LABEL_52;
        }
        if ( v5 <= v28 || v5 <= v29 || v5 <= v27 )
        {
          if ( v29 <= v5 || v29 <= v28 || v29 <= v27 )
            goto LABEL_49;
          goto LABEL_47;
        }
      }
      if ( v31 == 0 )
      {
        LOBYTE(v5) = 19;
        v26 = v24;
        goto LABEL_52;
      }
      v33 = *(_BYTE *)(*(int *)(*(_QWORD *)(v31 + 8) + 8LL) + v31 + 90);
      LOBYTE(v5) = 19;
      v26 = v24;
      goto LABEL_51;
    }
  }
  return (unsigned int)v5;
}
