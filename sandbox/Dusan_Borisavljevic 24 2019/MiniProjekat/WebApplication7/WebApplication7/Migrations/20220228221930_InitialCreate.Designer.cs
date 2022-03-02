﻿// <auto-generated />
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Metadata;
using Microsoft.EntityFrameworkCore.Migrations;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;
using WebApplication7.Models;

namespace WebApplication7.Migrations
{
    [DbContext(typeof(DetaljiPlacanjaContext))]
    [Migration("20220228221930_InitialCreate")]
    partial class InitialCreate
    {
        protected override void BuildTargetModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder
                .UseIdentityColumns()
                .HasAnnotation("Relational:MaxIdentifierLength", 128)
                .HasAnnotation("ProductVersion", "5.0.0");

            modelBuilder.Entity("WebApplication7.Models.PaymentDetail", b =>
                {
                    b.Property<int>("idkartice")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("int")
                        .UseIdentityColumn();

                    b.Property<string>("broj_kartice")
                        .HasColumnType("nvarchar(16)");

                    b.Property<string>("datum_do_kad_vazi")
                        .HasColumnType("nvarchar(5)");

                    b.Property<string>("ime_vlasnika_kartice")
                        .HasColumnType("nvarchar(100)");

                    b.Property<string>("sigurnosni_kod")
                        .HasColumnType("nvarchar(3)");

                    b.HasKey("idkartice");

                    b.ToTable("PaymentDetails");
                });
#pragma warning restore 612, 618
        }
    }
}
