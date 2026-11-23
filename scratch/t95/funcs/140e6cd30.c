// THUNK ALIAS -> sub_143C41710 (jmp:0x140e6cd30->0x143c41710)
__int64 __fastcall sub_143C41710(__int64 a1)
{
  __int64 *v1; // rax
  __int64 v2; // rdx
  int v3; // esi
  __int64 v4; // rbx
  char v5; // bp
  __int64 v6; // rbx
  unsigned int v7; // ebp
  bool v8; // cc
  char v9; // bl
  char v10; // bl
  __int64 v11; // rsi
  __int64 v12; // rdi
  __int64 v13; // r8
  char v14; // r8
  __int64 v15; // rax
  __int64 v16; // rax
  __int64 v17; // rax
  char v18; // al

  v1 = *(__int64 **)(a1 + 24);
  v2 = *(_QWORD *)(a1 + 32);
  LOWORD(v3) = 1500;
  if ( v1 == (__int64 *)v2 )
  {
    v5 = 0;
LABEL_14:
    v10 = (__int16)v3 >= 5500;
    goto LABEL_15;
  }
  v4 = *v1;
  v5 = 0;
  if ( *v1 == 0 )
    goto LABEL_14;
  if ( *(_QWORD *)(v4 + 48) != 0 )
  {
    v6 = *(_QWORD *)(v4 + 80);
    if ( v6 != 0 )
    {
      v7 = ((unsigned int)(26215 * *(__int16 *)(v6 + 384)) >> 31) + ((26215 * *(__int16 *)(v6 + 384)) >> 18);
      v8 = *(__int16 *)(v6 + 384) / 10 < 2;
      v9 = 1;
      if ( !v8 )
        v9 = v7;
      v5 = v9 / 8;
    }
  }
  if ( *v1 == 0 )
    goto LABEL_14;
  v3 = *(__int16 *)(*v1 + 168);
  v10 = 10;
  if ( v3 <= 9499 )
  {
    v10 = 7;
    if ( (__int16)v3 <= 8999 )
    {
      v10 = 4;
      if ( (__int16)v3 <= 7999 )
        goto LABEL_14;
    }
  }
LABEL_15:
  v11 = *(_QWORD *)(a1 + 216);
  if ( v11 != 0
    && (*(_BYTE *)(a1 + 185) != 0 && (v12 = *(_QWORD *)(v11 + 272)) != 0 || (v12 = *(_QWORD *)(v11 + 264)) != 0) )
  {
    if ( v1 == (__int64 *)v2 || (v2 = *v1, *v1 == 0) )
    {
      LODWORD(v11) = 0;
      goto LABEL_38;
    }
    LODWORD(v2) = *(__int16 *)(v2 + 168);
    if ( (int)v2 < 8000 )
    {
      LODWORD(v11) = 0;
    }
    else
    {
      v13 = *(_QWORD *)(v12 + 24);
      LOWORD(v2) = 1500;
      if ( v13 != *(_QWORD *)(v12 + 32) && *(_QWORD *)v13 != 0 )
        LOWORD(v2) = *(_WORD *)(*(_QWORD *)v13 + 168LL);
      v14 = *(_BYTE *)(v11 + 460);
      if ( v14 == 3 )
        LOWORD(v2) = (__int16)v2 / 3;
      if ( v14 == 2 )
        LODWORD(v2) = (unsigned int)(__int16)(v2 + ((unsigned __int16)v2 >> 15)) >> 1;
      LODWORD(v2) = (__int16)v2;
      LOBYTE(v11) = 2;
      if ( (__int16)v2 <= 8999 )
        LOBYTE(v11) = (__int16)v2 >= 8000;
    }
  }
  else
  {
    LODWORD(v11) = 0;
    if ( v1 == (__int64 *)v2 )
      goto LABEL_38;
  }
  v15 = *v1;
  if ( v15 != 0 && *(_QWORD *)(v15 + 152) != 0 )
    v10 += *(__int16 *)(v15 + 168) >= 8000;
LABEL_38:
  LOBYTE(v2) = 100;
  v16 = sub_1411D9CF0(a1, v2, 0, 1, 1);
  if ( v16 != 0 )
  {
    v17 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v16 + 1688LL))(v16);
    if ( v17 != 0 )
    {
      v18 = *(_BYTE *)(v17 + 25);
      if ( v18 <= 16 )
        v10 -= v18 < 5;
      else
        ++v10;
    }
  }
  LOBYTE(v11) = v10 + v5 + v11;
  return (unsigned int)v11;
}
