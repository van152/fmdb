__int64 *__fastcall sub_14081EDF0(__int64 a1, __int64 *a2)
{
  __int64 v4; // rdi
  int v5; // eax
  __int64 v6; // r8
  volatile signed __int32 *v7; // rcx
  __int64 v8; // rsi
  volatile signed __int32 *v9; // rcx
  volatile signed __int32 *v10; // rcx
  unsigned int *v11; // r15
  __int64 v12; // rdx
  int v13; // r13d
  volatile signed __int32 *v14; // r12
  volatile signed __int32 *v15; // rdi
  __int64 v16; // rsi
  int v17; // eax
  int v18; // ebx
  unsigned int *v19; // r13
  char *v20; // r15
  __int64 v21; // rdx
  int v22; // eax
  int v23; // esi
  char *v24; // r14
  int v25; // eax
  volatile signed __int32 *v26; // rax
  volatile signed __int32 *v27; // rcx
  volatile signed __int32 *v28; // rcx
  int v29; // r8d
  volatile signed __int32 *v30; // rdx
  volatile signed __int32 *v31; // rcx
  __int64 *v33; // [rsp+28h] [rbp-48h]
  int v34; // [rsp+34h] [rbp-3Ch]
  volatile signed __int32 *v35; // [rsp+38h] [rbp-38h] BYREF
  int v36; // [rsp+44h] [rbp-2Ch]
  char v37[8]; // [rsp+48h] [rbp-28h] BYREF
  volatile signed __int32 *v38; // [rsp+50h] [rbp-20h] BYREF
  unsigned int v39; // [rsp+58h] [rbp-18h] BYREF
  volatile signed __int32 *v40; // [rsp+60h] [rbp-10h] BYREF
  int v41; // [rsp+6Ch] [rbp-4h]
  __int64 v42; // [rsp+70h] [rbp+0h]

  v42 = -2;
  v4 = qword_141ABD468;
  sub_140805C50(&v35, a1 + 8);
  v5 = *(_DWORD *)(*(_QWORD *)(v4 + 8) + 264LL);
  if ( (v5 & 1) != 0 && *(_QWORD *)a1 != 0 )
  {
    v6 = *(unsigned int *)(a1 + 24);
    if ( (_DWORD)v6 != -1 )
    {
      sub_14080B990(&v40, 0x14193C89FLL, v6);
      sub_140806120(&v35, &v40);
      v7 = v40;
      if ( v40 != nullptr && _InterlockedDecrement(v40 - 1) == 0 )
        sub_1412EC9A0((__int64)(v7 - 1));
      v5 = *(_DWORD *)(*(_QWORD *)(v4 + 8) + 264LL);
    }
  }
  if ( (v5 & 8) != 0 )
  {
    v38 = nullptr;
    v8 = sub_1412EC810(264, 3);
    *(_QWORD *)v8 = 0x300000000LL;
    *(_DWORD *)(v8 + 8) = 2829099;
    v9 = v38 - 1;
    if ( v38 != nullptr && _InterlockedDecrement(v9) == 0 )
      sub_1412EC9A0((__int64)v9);
    v38 = nullptr;
    _InterlockedIncrement((volatile signed __int32 *)v8);
    v38 = (volatile signed __int32 *)(v8 + 4);
    sub_140805C50(&v40, &v38);
    v33 = a2;
    v10 = v38;
    if ( v38 != nullptr && _InterlockedDecrement(v38 - 1) == 0 )
      sub_1412EC9A0((__int64)(v10 - 1));
    v38 = v35;
    v11 = &v39;
    v39 = 0;
    v12 = 0;
    v13 = v36;
    v34 = v36;
    while ( (_DWORD)v12 != v13 )
    {
      v14 = v38;
      v15 = v38 + 2;
      v16 = (unsigned int)sub_140811DC0(v38 + 2, v12);
      sub_14080F1F0(v37, v16);
      v17 = sub_141758DB0(v37);
      v18 = v17;
      if ( v17 > 0 )
      {
        sub_140807AB0(&v40, (unsigned int)v17);
        if ( v40 != nullptr )
        {
          v19 = v11;
          v20 = (char *)v40 + v41;
          sub_141758A00();
          v20[v18 + 8] = 0;
          v11 = v19;
          v13 = v34;
          v41 += v18;
        }
      }
      v21 = 224;
      switch ( (int)v16 )
      {
        case 'A':
          v21 = 192;
          goto LABEL_31;
        case 'E':
          v21 = 203;
          goto LABEL_31;
        case 'I':
          v21 = 206;
          goto LABEL_31;
        case 'O':
          v21 = 336;
          goto LABEL_31;
        case 'U':
          v21 = 218;
          goto LABEL_31;
        case 'a':
          goto LABEL_31;
        case 'e':
          v21 = 235;
          goto LABEL_31;
        case 'i':
          v21 = 238;
          goto LABEL_31;
        case 'o':
          v21 = 337;
          goto LABEL_31;
        case 'u':
          v21 = 250;
LABEL_31:
          sub_14080F1F0(v37, v21);
          v22 = sub_141758DB0(v37);
          v23 = v22;
          if ( v22 > 0 )
          {
            sub_140807AB0(&v40, (unsigned int)v22);
            if ( v40 != nullptr )
            {
              v24 = (char *)v40 + v41;
              sub_141758A00();
              v24[v23 + 8] = 0;
              v41 += v23;
            }
          }
          break;
        default:
          break;
      }
      sub_140811B30(v15, v11, *((unsigned int *)v14 + 1));
      v12 = v39;
    }
    sub_140807AB0(&v40, 3);
    if ( v40 != nullptr )
    {
      *(volatile signed __int32 *)((char *)v40 + v41 + 8) = 4210752;
      v25 = v41 + 3;
      v41 += 3;
      a2 = v33;
      if ( v40 != nullptr )
      {
        *((_DWORD *)v40 + 1) = v25;
        v26 = v40;
        v38 = nullptr;
        if ( v40 != nullptr )
        {
          _InterlockedIncrement(v40);
          v38 = v26 + 1;
        }
        goto LABEL_40;
      }
    }
    else
    {
      a2 = v33;
    }
    v38 = nullptr;
LABEL_40:
    sub_140806590(&v35, 1024);
    sub_140806120(&v35, &v38);
    v27 = v38;
    if ( v38 != nullptr && _InterlockedDecrement(v38 - 1) == 0 )
      sub_1412EC9A0((__int64)(v27 - 1));
    v28 = v40;
    if ( v40 != nullptr && _InterlockedDecrement(v40) == 0 )
      sub_1412EC9A0((__int64)v28);
  }
  if ( v35 != nullptr )
  {
    v29 = v36;
    v30 = v35 + 2;
    *a2 = 0;
    sub_140809040(a2, (__int64)v30, v29);
    v31 = v35;
    if ( v35 != nullptr && _InterlockedDecrement(v35) == 0 )
      sub_1412EC9A0((__int64)v31);
  }
  else
  {
    *a2 = 0;
  }
  return a2;
}
