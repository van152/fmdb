__int64 __fastcall sub_143D24170(__int64 a1, int a2, unsigned int a3)
{
  volatile signed __int32 **v6; // r14
  __int64 v7; // r8
  volatile signed __int32 *v8; // rdi
  __int64 v9; // rbp
  volatile signed __int32 *v10; // rbx
  int v11; // ebx
  __int64 *v12; // rax
  __int64 *v13; // rcx
  __int64 *v14; // rdx
  __int64 *v15; // rdi
  __int64 v16; // rcx
  void (__fastcall ***v17)(_QWORD, __int64); // rcx
  volatile signed __int32 *v18; // rcx
  __int64 v19; // rcx
  volatile signed __int32 *v21; // [rsp+48h] [rbp-60h] BYREF
  int v22; // [rsp+54h] [rbp-54h] BYREF
  unsigned int v23; // [rsp+58h] [rbp-50h] BYREF
  volatile signed __int32 *v24; // [rsp+60h] [rbp-48h] BYREF
  _QWORD v25[8]; // [rsp+68h] [rbp-40h] BYREF

  v25[0] = 0;
  sub_14080D0E0(a1: &v23, a2: 0x1418E2C24LL);
  LODWORD(v6) = 0;
  LOBYTE(v7) = 1;
  sub_140FFADB0(a1, a2: v25, a3: v7, a4: 0);
  v21 = (volatile signed __int32 *)0x80100004E554C4CLL;
  sub_1407D0F70(
    a1: (unsigned int)&v21,
    a2: (unsigned int)&v24,
    a3: a2,
    a4: (unsigned int)v25,
    a5: (__int64)&v23,
    a6: 0,
    a7: 0,
    0);
  if ( v24 == nullptr )
    goto LABEL_30;
  v21 = v24;
  _InterlockedIncrement(v24 + 2);
  v8 = v21;
  (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)v21 + 40LL))(
    a1: v21,
    a2: &v23,
    a3: 4);
  if ( *((_DWORD *)v8 + 4) != 0 )
  {
LABEL_3:
    LODWORD(v6) = 0;
    goto LABEL_24;
  }
  if ( v23 != 0 )
  {
    v9 = 0;
    v6 = &v21;
    while ( 1 )
    {
      v22 = v9;
      v10 = v21;
      (*(void (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)v21 + 40LL))(
        a1: v21,
        a2: &v22,
        a3: 4);
      if ( *((_DWORD *)v10 + 4) != 0 )
        goto LABEL_3;
      v11 = v22;
      if ( *(_QWORD *)(a1 + 40) == 0
        && (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a1 + 48LL))(a1) > (unsigned __int64)v11 )
      {
        goto LABEL_19;
      }
      v12 = *(__int64 **)(a1 + 32);
      v13 = (__int64 *)v12[1];
      v14 = v12;
      if ( *((_BYTE *)v13 + 25) == 0 )
      {
        v14 = *(__int64 **)(a1 + 32);
        do
        {
          v15 = v13 + 2;
          if ( *((_DWORD *)v13 + 7) >= v11 )
          {
            v14 = v13;
            v15 = v13;
          }
          v13 = (__int64 *)*v15;
        }
        while ( *(_BYTE *)(*v15 + 25) == 0 );
      }
      if ( *((_BYTE *)v14 + 25) == 0 && *((_DWORD *)v14 + 7) <= v11 )
        break;
LABEL_15:
      v16 = 0;
LABEL_21:
      if ( (unsigned __int8)sub_140E5DC10(a1: v16, a2: &v21, a3) == 0 )
        goto LABEL_3;
      if ( ++v9 >= (unsigned __int64)v23 )
        goto LABEL_23;
    }
    v16 = 0;
    if ( v14 == v12 )
      goto LABEL_21;
    v11 = *((_DWORD *)v14 + 8);
LABEL_19:
    if ( v11 >= 0 )
    {
      v16 = *(_QWORD *)(**(_QWORD **)(a1 + 128) + 8LL * (unsigned int)v11);
      goto LABEL_21;
    }
    goto LABEL_15;
  }
LABEL_23:
  *(_BYTE *)(a1 + 91) = 0;
  LOBYTE(v6) = 1;
LABEL_24:
  v17 = (void (__fastcall ***)(_QWORD, __int64))v21;
  if ( v21 != nullptr && _InterlockedDecrement(v21 + 2) == 0 )
    (**v17)(a1: v17, a2: 1);
  v18 = v24;
  if ( v24 != nullptr && _InterlockedDecrement(v24 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v18)(a1: v18, a2: 1);
LABEL_30:
  v19 = v25[0];
  if ( v25[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v25[0] - 4LL)) == 0 )
    sub_1412EC9A0(a1: v19 - 4);
  return (unsigned int)v6;
}
