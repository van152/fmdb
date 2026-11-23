__int64 __fastcall sub_1411D7790(__int64 a1, int *a2, _DWORD *a3, __int64 a4, char a5)
{
  __int64 v5; // rax
  unsigned __int64 v7; // rbx
  _QWORD *v8; // r12
  __int64 v9; // rcx
  __int64 v10; // rsi
  bool v11; // zf
  __int64 v12; // rbp
  __int64 v13; // r13
  _QWORD *v14; // r15
  __int64 v15; // rcx
  __int64 v16; // r14
  __int64 v17; // rax
  __int64 v18; // rax
  __int64 v19; // rax
  __int64 v20; // rsi
  __int64 v21; // rax
  __int64 v22; // rax
  __int64 i; // rcx
  int v24; // eax
  __int64 v25; // rax
  __int64 v26; // r8
  __int64 v27; // rdx
  __int64 v28; // rcx
  int v29; // r9d
  int v30; // eax
  __int64 v32; // [rsp+20h] [rbp-B8h]
  int v33; // [rsp+54h] [rbp-84h]
  __int64 v34; // [rsp+58h] [rbp-80h]
  int v35; // [rsp+60h] [rbp-78h] BYREF
  int v36; // [rsp+68h] [rbp-70h] BYREF
  __int64 v37; // [rsp+70h] [rbp-68h]
  __int64 v38; // [rsp+78h] [rbp-60h]
  _DWORD *v39; // [rsp+80h] [rbp-58h]
  int *v40; // [rsp+88h] [rbp-50h]
  __int64 v41; // [rsp+90h] [rbp-48h]

  v39 = a3;
  *a3 = 1;
  *a2 = -1;
  v5 = *(_QWORD *)(a1 + 24);
  if ( *(_QWORD *)(a1 + 32) != v5 )
  {
    v40 = a2;
    v37 = a4;
    v34 = 0;
    v33 = 0;
    v7 = 0;
    while ( 1 )
    {
      v8 = *(_QWORD **)(v5 + 8 * v7);
      if ( v8 != nullptr )
      {
        if ( a5 != 0 )
        {
          v9 = 0;
        }
        else
        {
          if ( byte_141B595A8 != 0 )
          {
            v10 = qword_141B595B0;
            v11 = v10 == (unsigned int)MEMORY[0x141947498]();
          }
          else
          {
            v11 = qword_141B5A658 == (unsigned int)MEMORY[0x141947498]();
          }
          v9 = *(_QWORD *)(v8[20] + 184LL);
          if ( v11 && v9 == 0 )
          {
            *(_QWORD *)(v8[20] + 184LL) = sub_140B530F0(v8);
            v9 = *(_QWORD *)(v8[20] + 184LL);
          }
        }
        v38 = v9;
        v12 = v8[7];
        v13 = v8[8];
        if ( v12 != v13 )
          break;
      }
LABEL_3:
      ++v7;
      v5 = *(_QWORD *)(a1 + 24);
      if ( v7 >= (*(_QWORD *)(a1 + 32) - v5) >> 3 )
        return v34;
    }
    v41 = v38 + 76;
    while ( 1 )
    {
      v14 = *(_QWORD **)v12;
      v15 = *(_QWORD *)v12 + *(int *)(*(_QWORD *)(*(_QWORD *)v12 + 8LL) + 4LL) + 8LL;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v15 + 1312LL))(v15) == 0
        && (*(unsigned __int8 (__fastcall **)(_QWORD *))(*v14 + 664LL))(v14) == 0 )
      {
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD *))(*v14 + 640LL))(v14) == 0 )
          goto LABEL_15;
        v16 = (__int64)v14 + *(int *)(v14[1] + 4LL) + 8;
        v17 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v16 + 656LL))(v16);
        if ( v17 != 0 && *(_BYTE *)(v17 + 47) == 0 )
        {
          v18 = *(_QWORD *)(v17 + 48);
          if ( v18 != 0 && v18 == v8[6] )
          {
            v19 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v16 + 992LL))(v16);
            if ( v19 != 0 )
              break;
          }
        }
      }
LABEL_16:
      v12 += 8;
      if ( v12 == v13 )
        goto LABEL_3;
    }
    v20 = v19;
    if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v19 + 144LL))(v19) != 0 )
    {
      v21 = *(_QWORD *)(v20 + 16);
      if ( v21 != 0 && *(_BYTE *)(v21 + 47) == 0 )
      {
        v22 = *(_QWORD *)(v21 + 48);
        if ( v22 != 0 )
        {
          for ( i = *(_QWORD *)(v22 + 280); i != *(_QWORD *)(v22 + 288); i += 8 )
          {
            if ( *(_QWORD *)(*(_QWORD *)i + 8LL) == v22 && *(_BYTE *)(*(_QWORD *)i + 48LL) == 18 )
              goto LABEL_16;
          }
        }
      }
    }
LABEL_15:
    v36 = 124518401;
    LOBYTE(v32) = 25;
    if ( (*(__int64 (__fastcall **)(_QWORD *, int *, _QWORD, _QWORD, __int64))(*v14 + 560LL))(v14, &v36, 0, 0, v32) == 0 )
    {
      if ( a5 != 0
        || (*(__int64 (__fastcall **)(_QWORD *, _QWORD, _QWORD, _QWORD))(*v14 + 592LL))(v14, 0, 0, 0) == 0
        && (v38 == 0
         || (v32 = 0, (*(unsigned __int8 (__fastcall **)(_QWORD *, _QWORD *, __int64))(*v14 + 696LL))(v14, v8, v41) != 0)) )
      {
        v11 = (*(__int64 (__fastcall **)(_QWORD *))(*v14 + 800LL))(v14) == 0;
        v24 = v33;
        if ( !v11 )
        {
          v25 = (*(__int64 (__fastcall **)(_QWORD *))(*v14 + 800LL))(v14);
          LOBYTE(v26) = 1;
          sub_14085D840(v25, &v35, v26);
          v24 = v35;
        }
        if ( v24 != 0 )
        {
          v33 = v24;
          v27 = v37;
          if ( v37 == 0
            || (v28 = v37 + *(int *)(*(_QWORD *)(v37 + 8) + 4LL) + 8,
                (_QWORD *)(*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v28 + 1680LL))(v28) != v14) )
          {
            LOBYTE(v27) = 12;
            if ( (v33 & (*(unsigned int (__fastcall **)(_QWORD *, __int64))(*v14 + 1128LL))(v14, v27)) != 0 )
            {
              LOBYTE(v29) = 2;
              v30 = sub_1410C2810((_DWORD)v14, v33, 0, v29, v37, 0, 0, 0);
              if ( v30 > 0 )
                ++*v39;
              if ( v30 > *v40 )
              {
                *v40 = v30;
                v34 = (__int64)v14 + *(int *)(v14[1] + 4LL) + 8;
              }
            }
          }
        }
        else
        {
          v33 = 0;
        }
      }
    }
    goto LABEL_16;
  }
  return 0;
}
