char __fastcall sub_141039400(__int64 a1, int a2, __int64 *a3)
{
  _QWORD *v6; // r14
  __int64 v7; // rax
  _DWORD *v8; // rcx
  __int64 v9; // rax
  unsigned __int64 v10; // rax
  __int64 v11; // rcx
  int v12; // eax
  int v13; // edi
  __int64 v14; // rax
  unsigned __int64 v15; // rax
  __int64 v16; // rcx
  __int64 *v17; // rdi
  __int64 v18; // rax
  __int64 v19; // rcx
  unsigned __int64 v20; // rax
  __int64 v21; // rcx
  int v22; // edi
  unsigned __int64 v23; // rax
  __int64 v24; // rcx
  __int64 v25; // rcx
  int v26; // eax
  int v27; // ecx
  int v28; // edi
  unsigned __int64 v29; // rax
  __int64 v30; // rcx
  __int16 v31; // di
  unsigned __int64 v32; // rax
  __int64 v33; // rcx
  int v34; // edi
  unsigned __int64 v35; // rax
  __int64 v36; // rcx
  int v37; // edi
  unsigned __int64 v38; // rax
  __int64 v39; // rcx
  unsigned __int64 v41; // [rsp+28h] [rbp-18h] BYREF
  _QWORD v42[6]; // [rsp+30h] [rbp-10h] BYREF

  v42[1] = -2;
  if ( a2 <= 1281977957 )
  {
    if ( a2 > 1281778028 )
    {
      if ( a2 == 1281778029 )
      {
        v37 = *(__int16 *)(a1 + 52);
        v14 = sub_14083D4F0(a1) + 40;
        LODWORD(v42[0]) = v37;
        v41 = v14;
        if ( &v41 != (unsigned __int64 *)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v38 = v41;
          v39 = v42[0];
          a3[1] = v42[0];
          *a3 = v38;
          v14 = sub_14083D4F0(v39) + 8;
          v42[0] = 0;
          v41 = v14;
        }
        goto LABEL_52;
      }
      if ( a2 == 1281847919 )
      {
        v22 = *(__int16 *)(a1 + 54);
        v14 = sub_14083D4F0(a1) + 40;
        LODWORD(v42[0]) = v22;
        v41 = v14;
        if ( &v41 != (unsigned __int64 *)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v23 = v41;
          v24 = v42[0];
          a3[1] = v42[0];
          *a3 = v23;
          v14 = sub_14083D4F0(v24) + 8;
          v42[0] = 0;
          v41 = v14;
        }
        goto LABEL_52;
      }
    }
    else
    {
      if ( a2 == 1145392197 )
      {
        v31 = *(_WORD *)(a1 + 52);
        v14 = sub_14083D4F0(a1) + 24;
        LOBYTE(v42[0]) = v31 == -1;
        v41 = v14;
        if ( &v41 != (unsigned __int64 *)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v32 = v41;
          v33 = v42[0];
          a3[1] = v42[0];
          *a3 = v32;
          v14 = sub_14083D4F0(v33) + 8;
          v42[0] = 0;
          v41 = v14;
        }
        goto LABEL_52;
      }
      if ( a2 == 1281648230 )
      {
        v13 = *(char *)(a1 + 60);
        v14 = sub_14083D4F0(a1) + 40;
        LODWORD(v42[0]) = v13;
        v41 = v14;
        if ( &v41 != (unsigned __int64 *)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v15 = v41;
          v16 = v42[0];
          a3[1] = v42[0];
          *a3 = v15;
          v14 = sub_14083D4F0(v16) + 8;
          v42[0] = 0;
          v41 = v14;
        }
        goto LABEL_52;
      }
    }
  }
  else
  {
    if ( a2 > 1282302323 )
    {
      if ( a2 == 1282302324 )
      {
        v25 = *(_QWORD *)(a1 + 40);
        if ( v25 != 0 )
        {
          v26 = *(_DWORD *)(v25 + 12);
          v27 = *(_DWORD *)(v25 + 16);
          if ( v27 == 0 )
            v27 = v26;
        }
        else
        {
          v26 = -1;
          v27 = -1;
        }
        v41 = __PAIR64__(v27, v26);
        sub_140FE72B0(&v41, 1315856756, a3);
        return 1;
      }
      if ( a2 != 1282635106 )
      {
        if ( a2 == 1684172397 )
        {
          v6 = (_QWORD *)(a1 + 24);
          v7 = sub_14083D4F0(a1);
          v42[0] = 0;
          if ( v42 != v6 )
          {
            v8 = (_DWORD *)*v6;
            if ( *v6 != 0 )
              _InterlockedIncrement(v8 - 1);
            v42[0] = v8;
          }
          v9 = v7 + 136;
          v41 = v9;
          if ( &v41 != (unsigned __int64 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v10 = v41;
            v11 = v42[0];
            a3[1] = v42[0];
            *a3 = v10;
            v9 = sub_14083D4F0(v11) + 8;
            v42[0] = 0;
            v41 = v9;
          }
          (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v9 + 16LL))(v9, &v41);
          if ( *v6 == 0 || *(_DWORD *)*v6 == 0 )
          {
            v12 = *(_DWORD *)(a1 + 48);
            if ( v12 == 1000004 )
            {
              sub_14083D9C0(&v41, 0x141931D4BLL);
              sub_14083DFA0(a3, &v41);
              (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v41 + 16LL))(v41, &v41);
            }
            else if ( v12 == 1000001 )
            {
              sub_14083D9C0(&v41, 0x1418FF43ELL);
              sub_14083DFA0(a3, &v41);
              (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v41 + 16LL))(v41, &v41);
            }
          }
        }
        return sub_140FE3F20((_DWORD *)a1, a2, a3);
      }
      v28 = *(__int16 *)(a1 + 56);
      v14 = sub_14083D4F0(a1) + 40;
      LODWORD(v42[0]) = v28;
      v41 = v14;
      if ( &v41 != (unsigned __int64 *)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v29 = v41;
        v30 = v42[0];
        a3[1] = v42[0];
        *a3 = v29;
        v14 = sub_14083D4F0(v30) + 8;
        v42[0] = 0;
        v41 = v14;
      }
LABEL_52:
      (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v14 + 16LL))(v14, &v41);
      return 1;
    }
    if ( a2 == 1281977958 )
    {
      v34 = *(char *)(a1 + 59);
      v14 = sub_14083D4F0(a1) + 40;
      LODWORD(v42[0]) = v34;
      v41 = v14;
      if ( &v41 != (unsigned __int64 *)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v35 = v41;
        v36 = v42[0];
        a3[1] = v42[0];
        *a3 = v35;
        v14 = sub_14083D4F0(v36) + 8;
        v42[0] = 0;
        v41 = v14;
      }
      goto LABEL_52;
    }
    if ( a2 == 1282302317 )
    {
      v17 = (__int64 *)(a1 + 24);
      v18 = sub_14083D4F0(a1);
      v42[0] = 0;
      if ( v42 != v17 )
      {
        v19 = *v17;
        if ( *v17 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v19 - 4));
        v42[0] = v19;
      }
      v14 = v18 + 136;
      v41 = v14;
      if ( &v41 != (unsigned __int64 *)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v20 = v41;
        v21 = v42[0];
        a3[1] = v42[0];
        *a3 = v20;
        v14 = sub_14083D4F0(v21) + 8;
        v42[0] = 0;
        v41 = v14;
      }
      goto LABEL_52;
    }
  }
  return sub_140FE3F20((_DWORD *)a1, a2, a3);
}
